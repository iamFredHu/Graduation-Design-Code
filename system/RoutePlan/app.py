from flask_cors import *
from flask import *
from flask_bootstrap import Bootstrap
import json
import random
from TSP_edges import *
from nx_draw_old import *
import pymysql

connect = pymysql.connect(
    host='127.0.0.1',
    port=3306,
    user='root',
    passwd='mysql',
    db='MapData',
    charset='utf8'
)

app = Flask(__name__)
Bootstrap(app)

def my_method(m, nodelist, D, Data, v, t_max, e, wmax, supply):
    n = len(D)
    w = []
    s = []
    for _ in range(m):
        w.append(wmax)

    s = [x for x in supply]

    tolerance = time_initCheck(D, Data, v, e)

    path = [[] for _ in range(m)]  # 每一个无人机的路径
    T = [[0] for _ in range(m)]  # 每一个无人机路径的累积飞行时间

    visited = [0 for _ in range(n)]  # 标记POI是否被访问
    effective = [0 for _ in range(n)]  # 标记POI是否被有效访问(在允许时间内访问)
    onTime = [0 for _ in range(n)]  # 标记POI是否被准时访问

    P_0 = 0  # 起点（基站）
    nodelist.remove(P_0)  # 去掉起点（基站）
    for k in range(m):

        # T_remain = t_max  # 无人机剩余的续航时间
        Tr = [x * 60 for x in Data]  # Tr为各POI剩余访问时间,将分钟换成秒

        while len(nodelist) and (P_0 not in path[k]):
            cost = [math.inf for _ in range(n)]  # 记录选择每一个POI的cost
            t_f = [0 for _ in range(n)]  # 记录选择每一个POI的飞行时间
            t_f_r = [0 for _ in range(n)]  # 记录选择每一个POI且飞回起点的飞行时间
            for i in nodelist:  # 对nodelist里现有的每一个POI
                # 判断该poi是否可达，需要计算该poi的t_f和t_f_r
                # angle = 0
                if (len(path[k]) == 0):  # 从起点出发，选择第一个POI
                    t_f[i] = D[0][i] / v
                    t_f_r[i] = 2 * t_f[i]  # 修改标记
                else:
                    t_f[i] = D[path[k][-1]][i] / v
                    t_r_i = D[i][0] / v  # 修改标记
                    t_f_r[i] = t_f[i] + t_r_i

                # 判断该poi是否可达
                T_remain = t_max - T[k][-1]  # 剩余的续航时间
                tr_remain = Tr[i] - t_f[i]  # 飞过去后，该POI的剩余访问时间

                if tr_remain < 0 and math.fabs(tr_remain) > tolerance[i] * 60:
                    cost[i] = math.inf  # 该POI已经死了，不可达，代价置为无穷大
                else:  # 该POI还活着
                    if t_f_r[i] > T_remain:  # 剩余续航时间不足以选该POI
                        cost[i] = math.inf  # 不可达，代价置为无穷大
                    else:
                        if s[i] > w[k]:
                            cost[i] = math.inf  # 不可达，代价置为无穷大
                        else:
                            # 计算该poi的cost
                            rou = 2
                            fai = T[k][-1] / t_max
                            # cost[i] =  t_f[i] +Tr[i]**(fai) + ((t_f_r[i] - t_f[i]) / fai) ** fai
                            cost[i] = t_f[i] + 2 * (Tr[i] ** (fai)) + s[i]
                            # cost[i] = t_f[i]

            # print(cost)
            p = cost.index(min(cost))  # 代价最小的POI编号 (如果全都是inf，会返回0，即回到起点)
            path[k].append(p)

            if p != 0:
                nodelist.remove(p)
                visited[p] = 1
                w[k] = w[k] - s[p]

                T[k].append(T[k][-1] + t_f[p])  # 访问新的poi后，计算当前总耗时，存于T[k]最后面
                for i in range(1, n):
                    Tr[i] = Tr[i] - t_f[p]  # 所有剩余访问时间变小
                if (T[k][-1] < Data[p] * 60 * (1 + e)):
                    effective[p] = 1
                if Tr[p] >= 0:
                    # if Tr[p] - T[k][-1]>=0:
                    onTime[p] = 1  # 剩余访问时间大于0，代表被准时访问。如果小于0，就是在20%内的不准时访问

            else:  # 代价最小的为起点，则返回起点（代价全inf情况）
                t_last = 0
                if (len(path[k]) >= 2):
                    t_last = D[path[k][-2]][0]
                T[k].append(T[k][-1] + t_last)  # 路径k最终用时，存于T[k]最后一项

        if k == m - 1:
            path[k].append(0)
            path[k - 1].append(0)
            T[k].append(T[k][-1] + t_last)
        path[k].insert(0, 0)  # 将起点加到路径最前面


    # 计算标准覆盖率（不考虑时间点的）
    coverage = 0
    for i in visited:
        coverage += i
    coverage_rate = coverage / (n - 1)

    # 计算有效覆盖率
    effective_coverage = 0
    for i in effective:
        effective_coverage += i
    effective_coverage_rate = effective_coverage / (n - 1)

    # 计算准时率
    punctual = 0
    for i in onTime:
        punctual += i
    onTime_rate = punctual / (n - 1)

    return path, effective_coverage_rate, onTime_rate

# 初始化数据，检查时间是否合理
def time_initCheck(D, Data, v, e):
    n = len(D)  # POI个数+1
    # print("--------")
    # print(n)
    tolerance = [0]  # 装POI的允许超时时间（min），即初始剩余访问时间的20%
    for i in range(1, n):
        t = D[0][i] / v  # 从起点直接飞过去的时间,单位：s
        t = t / 60  # 秒换成分钟
        tr_i = Data[i]
        if (tr_i < t):  # 剩余访问时间 比 直飞距离时间 小，是无法访问的，需重新设置剩余访问时间
            Data[i] = np.random.randint(t, 120 + 1)
        tolerance_i = Data[i] * e
        tolerance.append(tolerance_i)
    return tolerance


@app.route('/', methods=["post", "get"])
def index():  # put application's code here
    cursor = connect.cursor()

    # 数据的回传
    re_data = request.form.to_dict()
    if re_data != {}:
        if re_data['uavnum'] != '':
            cursor.execute("UPDATE Info SET uavnum='" + re_data['uavnum'] + "'WHERE id = 1;")
        if re_data['poinum'] != '':
            cursor.execute("UPDATE Info SET poinum='" + re_data['poinum'] + "'WHERE id = 1;")
        if re_data['tsmin'] != '':
            cursor.execute("UPDATE Info SET tsmin='" + re_data['tsmin'] + "'WHERE id = 1;")
        if re_data['tsmax'] != '':
            cursor.execute("UPDATE Info SET tsmax='" + re_data['tsmax'] + "'WHERE id = 1;")
        if re_data['uavspeed'] != '':
            cursor.execute("UPDATE Info SET uavspeed='" + re_data['uavspeed'] + "'WHERE id = 1;")
        if re_data['uavweight'] != '':
            cursor.execute("UPDATE Info SET uavweight='" + re_data['uavweight'] + "'WHERE id = 1;")
    connect.commit()

    cursor.execute("SELECT * FROM Info WHERE id = 1;")
    show_data = cursor.fetchone()
    show_m = show_data[2]
    show_n = show_data[1]
    show_tsmin = show_data[7]
    show_tsmax = show_data[8]
    show_speed = show_data[3]
    show_weight = show_data[6]

    return render_template('index.html', show_m=show_m, show_n=show_n, show_tsmin=show_tsmin, show_tsmax=show_tsmax,show_speed=show_speed,show_weight=show_weight)


@app.route('/show')
def show():  # put application's code here

    return render_template('map.html')

@app.route('/import', methods=["post", "get"])
def importdata():  # put application's code here
    cursor = connect.cursor()
    cursor.execute("SELECT * FROM Info WHERE id = 1;")
    show_data = cursor.fetchone()
    #0 id 1 poinum 2 uavnum 3 speed 4 续航时间 5 正方形区域边长 6 最大载重 7 8 tsmin tsmax
    show_n = show_data[1]
    show_m = show_data[2]
    show_tsmin = show_data[7]
    show_tsmax = show_data[8]
    show_speed = show_data[3]
    show_weight = show_data[6]

    return render_template('import.html',show_n=show_n,show_m=show_m,show_tsmin=show_tsmin,show_tsmax=show_tsmax,show_uavspeed=show_speed,show_uavweight=show_weight)


@app.route('/map_data', methods=["post", "get"])
def map_data():
    cursor = connect.cursor()
    cursor.execute("SELECT * from Info where id = 1")
    main_data = cursor.fetchone()

    n = int(main_data[1])
    m = int(main_data[2])

    v = float(main_data[3])  # 无人机飞行速度，25m/s = 90km/h
    t_max = float(main_data[4])  # 无人机续航时间，3h = 180min = 10800s
    # t_max = 7200 # 2h
    # t_max = 9000 # 2.5h
    # t_max = 14400 #4h
    S = int(main_data[5])  # 面积=S*S
    d = 1
    R = 2  # R >= [（根号2）/2] * d ,必须满足这个条件，这样一个圆盘才能包住一个网格
    wmax = float(main_data[6])  # 无人机的最大载重为100kg

    e = 0  # 容忍系数
    ts_min = int(main_data[7])  # 最小的ts值，即最短的要求访问时间
    ts_max = int(main_data[8])  # 最大的ts值，即最长的要求访问时间
    nodes = get_nodes(n, S, ts_min, ts_max)
    nodelist, coordinate, Data, supply = get_parameters(nodes)

    nodelist_copy = list(nodelist)
    pos = dict(zip(nodelist, coordinate))  # POI编号和坐标,包含基站

    D = get_distance_matrix(nodes)
    D *= 1000  # 千米换成米
    path, coverage_rate, onTime_rate = my_method(m, nodelist, D, Data, v, t_max, e, wmax, supply)
    edges = get_edges(path)

    coordinate_list = []
    for i in coordinate:
        coordinate_list.append(list(i))

    templine = []

    for i in range(len(path)):
        templist = []
        for j in path[i]:
            # templine[i].append(coordinate_list[j])
            templist.append(coordinate_list[j])
        templine.append(templist)

    class MapVal:
        mapline = templine

    freeuavflag = 0
    for i in templine:
        if len(i) > 2:
            freeuavflag += 1
    freeuavnum = m - freeuavflag
    if freeuavnum < 0:
        freeuavnum = 0

    data_list = {}

    colors = ["yellow", "purple", "red", "fuchsia", "dimgray", "darkorange", "tan", "silver", "forestgreen",
              "darkgreen", "royalblue", "navy", "darksalmon", "peru", "olive", "cyan", "mediumaquamarine", "skyblue",
              "indigo", "khaki"]
    symboltype = ['pin', 'triangle', 'rect', 'circle', 'diamond', 'arrow', 'roundRect']

    data_list['line_data'] = []
    data_list['poi'] = []
    data_list['center'] = [coordinate_list[0]]
    data_list['text'] = '在本次行动中，对兴趣点的有效覆盖率为{:.2%}。'.format(coverage_rate)+'空闲无人机的数量为：'+str(freeuavnum)

    for i in range(len(MapVal.mapline)):
        data_list['line_data'].append(
            {
                'data': MapVal.mapline[i],
                'type': 'line',
                'symbol': 'image://https://img.icons8.com/nolan/344/drone.png',
                'symbolSize': 50,
                'itemStyle': {
                    'borderWidth': 3,
                    'borderColor': colors[random.randint(0, 19)],
                    'color': colors[random.randint(0, 19)]
                }
            }
        )

    for j in coordinate:
        data_list['poi'].append(
            {
                'data': [list(j)],
                'type': 'line',
                'symbol': 'circle',
                'symbolSize': 40,
                'itemStyle': {
                    'borderWidth': 3,
                    'borderColor': '#EEEEEE',
                    'color': '#EEEEEE'
                }
            }
        )

    return Response(json.dumps(data_list), mimetype='application/json')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
    CORS(app, supports_credentials=True)
