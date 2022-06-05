from flask_cors import *
from flask import *
from flask_bootstrap import Bootstrap
import json
import random
from TSP_edges import *
from nx_draw_old import *
import pymysql
import random
from copy import deepcopy

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

    return render_template('index.html', show_m=show_m, show_n=show_n, show_tsmin=show_tsmin, show_tsmax=show_tsmax,
                           show_speed=show_speed, show_weight=show_weight)


@app.route('/show')
def show():  # put application's code here

    return render_template('map.html')


@app.route('/import', methods=["post", "get"])
def importdata():  # put application's code here
    cursor = connect.cursor()
    cursor.execute("SELECT * FROM Info WHERE id = 1;")
    show_data = cursor.fetchone()
    # 0 id 1 poinum 2 uavnum 3 speed 4 续航时间 5 正方形区域边长 6 最大载重 7 8 tsmin tsmax
    show_n = show_data[1]
    show_m = show_data[2]
    show_tsmin = show_data[7]
    show_tsmax = show_data[8]
    show_speed = show_data[3]
    show_weight = show_data[6]

    return render_template('import.html', show_n=show_n, show_m=show_m, show_tsmin=show_tsmin, show_tsmax=show_tsmax,
                           show_uavspeed=show_speed, show_uavweight=show_weight)


@app.route('/map_data', methods=["post", "get"])
def map_data():
    cursor = connect.cursor()
    cursor.execute("SELECT * from Info where id = 1")
    main_data = cursor.fetchone()
    geneNum = 500  # 种群数量
    generationNum = 500  # 迭代次数

    CENTER = 0  # 配送中心

    HUGE = 9999999
    VARY = 0.1  # 变异几率

    class Gene:
        def __init__(self, name='Gene', data=None):
            self.name = name
            self.length = n + m + 1
            if data is None:
                self.data = self._getGene(self.length)
            else:
                # assert(self.length+k == len(data))
                self.data = data
            self.fit, self.coverage_rate = self.getFit()
            self.chooseProb = 0  # 选择概率

        # randomly choose a gene
        def _generate(self, length):
            data = [i for i in range(1, length)]
            random.shuffle(data)
            # print(data)
            data.insert(0, CENTER)
            data.append(CENTER)
            # print(data)
            return data

        # insert zeors at proper positions
        def _insertZeros(self, data):
            flag = k
            sum = 0
            newData = []
            for index, pos in enumerate(data):
                sum += t[pos]
                if sum > Q:
                    newData.append(CENTER)
                    flag = flag - 1
                    sum = t[pos]
                    if flag == 0:
                        return newData
                newData.append(pos)
            return newData

        # return a random gene with proper center assigned
        def _getGene(self, length):
            data = self._generate(length)
            data = self._insertZeros(data)
            return data

        # return fitness
        def getFit(self):
            fit = distCost = timeCost = overloadCost = fuelCost = 0
            dist = []  # from this to next
            coverage_point = 0
            all_point = n
            # calculate distance
            i = 1
            while i < len(self.data):
                calculateDist = lambda x1, y1, x2, y2: math.sqrt(((x1 - x2) ** 2) + ((y1 - y2) ** 2))
                dist.append(calculateDist(X[self.data[i]], Y[self.data[i]], X[self.data[i - 1]], Y[self.data[i - 1]]))
                i += 1

            # distance cost
            distCost = sum(dist) * costPerKilo

            # time cost
            timeSpent = 0
            for i, pos in enumerate(self.data):
                # skip first center
                if i == 0:
                    continue
                # new car
                elif pos == CENTER:
                    timeSpent = 0
                # update time spent on road
                timeSpent += (dist[i - 1] / speed)
                # arrive early
                if timeSpent < eh[pos]:
                    timeCost += ((eh[pos] - timeSpent) * epu)
                    timeSpent = eh[pos]
                # arrive late
                elif timeSpent > lh[pos]:
                    timeCost += ((timeSpent - lh[pos]) * lpu)
                else:
                    coverage_point += 1
                # update time
                timeSpent += h[pos]

            # overload cost and out of fuel cost
            load = 0
            distAfterCharge = 0
            for i, pos in enumerate(self.data):
                # skip first center
                if i == 0:
                    continue
                # charge here
                if pos > n:
                    distAfterCharge = 0
                # at center, re-load
                elif pos == CENTER:
                    load = 0
                    distAfterCharge = 0
                # normal
                else:
                    load += t[pos]
                    distAfterCharge += dist[i - 1]
                    # update load and out of fuel cost
                    overloadCost += (HUGE * (load > Q))
                    fuelCost += (HUGE * (distAfterCharge > dis))

            fit = distCost + timeCost + overloadCost + fuelCost
            return 1 / fit, coverage_point / all_point

        def updateChooseProb(self, sumFit):
            self.chooseProb = self.fit / sumFit

        def moveRandSubPathLeft(self):
            path = random.randrange(k)  # choose a path index
            index = self.data.index(CENTER, path + 1)  # move to the chosen index
            # move first CENTER
            locToInsert = 0
            self.data.insert(locToInsert, self.data.pop(index))
            index += 1
            locToInsert += 1
            # move data after CENTER
            while self.data[index] != CENTER:
                self.data.insert(locToInsert, self.data.pop(index))
                index += 1
                locToInsert += 1
            # assert(self.length+k == len(self.data))

    def getSumFit(genes):
        sum = 0
        for gene in genes:
            sum += gene.fit
        return sum

    # return a bunch of random genes
    def getRandomGenes(size):
        genes = []
        for i in range(size):
            genes.append(Gene("Gene " + str(i)))
        return genes

    # 计算适应度和
    def getSumFit(genes):
        sumFit = 0
        for gene in genes:
            sumFit += gene.fit
        return sumFit

    # 更新选择概率
    def updateChooseProb(genes):
        sumFit = getSumFit(genes)
        for gene in genes:
            gene.updateChooseProb(sumFit)

    # 计算累计概率
    def getSumProb(genes):
        sum = 0
        for gene in genes:
            sum += gene.chooseProb
        return sum

    # 选择复制，选择前 1/3
    def choose(genes):
        num = int(geneNum / 6) * 2  # 选择偶数个，方便下一步交叉
        # sort genes with respect to chooseProb
        key = lambda gene: gene.chooseProb
        genes.sort(reverse=True, key=key)
        # return shuffled top 1/3
        return genes[0:num]

    # 交叉一对
    def crossPair(gene1, gene2, crossedGenes):
        gene1.moveRandSubPathLeft()
        gene2.moveRandSubPathLeft()
        newGene1 = []
        newGene2 = []
        # copy first paths
        centers = 0
        firstPos1 = 1
        for pos in gene1.data:
            firstPos1 += 1
            centers += (pos == CENTER)
            newGene1.append(pos)
            if centers >= 2:
                break
        centers = 0
        firstPos2 = 1
        for pos in gene2.data:
            firstPos2 += 1
            centers += (pos == CENTER)
            newGene2.append(pos)
            if centers >= 2:
                break
        # copy data not exits in father gene
        for pos in gene2.data:
            if pos not in newGene1:
                newGene1.append(pos)
        for pos in gene1.data:
            if pos not in newGene2:
                newGene2.append(pos)
        # add center at end
        newGene1.append(CENTER)
        newGene2.append(CENTER)
        # 计算适应度最高的
        key = lambda gene: gene.fit
        possible = []
        while gene1.data[firstPos1] != CENTER:
            newGene = newGene1.copy()
            newGene.insert(firstPos1, CENTER)
            newGene = Gene(data=newGene.copy())
            possible.append(newGene)
            firstPos1 += 1
        possible.sort(reverse=True, key=key)
        # assert(possible)
        crossedGenes.append(possible[0])
        key = lambda gene: gene.fit
        possible = []
        while gene2.data[firstPos2] != CENTER:
            newGene = newGene2.copy()
            newGene.insert(firstPos2, CENTER)
            newGene = Gene(data=newGene.copy())
            possible.append(newGene)
            firstPos2 += 1
        possible.sort(reverse=True, key=key)
        crossedGenes.append(possible[0])

    # 交叉
    def cross(genes):
        crossedGenes = []
        for i in range(0, len(genes), 2):
            crossPair(genes[i], genes[i + 1], crossedGenes)
        return crossedGenes

    # 合并
    def mergeGenes(genes, crossedGenes):
        # sort genes with respect to chooseProb
        key = lambda gene: gene.chooseProb
        genes.sort(reverse=True, key=key)
        pos = geneNum - 1
        for gene in crossedGenes:
            genes[pos] = gene
            pos -= 1
        return genes

    # 变异一个
    def varyOne(gene):
        varyNum = 10
        variedGenes = []
        for i in range(varyNum):
            p1, p2 = random.choices(list(range(1, len(gene.data) - 2)), k=2)
            newGene = gene.data.copy()
            newGene[p1], newGene[p2] = newGene[p2], newGene[p1]  # 交换
            variedGenes.append(Gene(data=newGene.copy()))
        key = lambda gene: gene.fit
        variedGenes.sort(reverse=True, key=key)
        return variedGenes[0]

    # 变异
    def vary(genes):
        for index, gene in enumerate(genes):
            # 精英主义，保留前三十
            if index < 30:
                continue
            if random.random() < VARY:
                genes[index] = varyOne(gene)
        return genes

    S = int(main_data[5])  # 正方形边长
    n = int(main_data[1])  # 客户点数量
    m = 0  # 充电站
    k = int(main_data[2])  # 车辆数量
    Q = float(main_data[6])  # 额定载重量, kg
    dis = float(main_data[4]) / 40  # 续航里程, km
    costPerKilo = 30  # 油价
    epu = 0  # 早到惩罚成本
    lpu = 999999999  # 晚到惩罚成本
    speed = float(main_data[3]) * 3.6  # 速度，km/h

    ts_min = int(main_data[7])  # 最小的ts值，即最短的要求访问时间
    ts_max = int(main_data[8])  # 最大的ts值，即最长的要求访问时间
    nodes = get_nodes(n, S, ts_min, ts_max)
    nodelist, coordinate, lh_min, t = get_parameters(nodes)

    nodelist_copy = list(nodelist)

    lh = []
    for i in lh_min:
        lh.append(i / 60)

    lh[0] = 1000 / 60

    X = []
    Y = []

    for i in range(n + 1):
        X.append(coordinate[i][0])
        Y.append(coordinate[i][1])

    # 遗留问题
    # 服务时间
    h = []
    for i in range(n + 1):
        h.append(0)
    # 最早到达时间
    eh = []
    for i in range(n + 1):
        eh.append(0)

    genes = getRandomGenes(geneNum)  # 初始种群
    # 迭代
    for i in range(generationNum):
        updateChooseProb(genes)
        sumProb = getSumProb(genes)
        chosenGenes = choose(deepcopy(genes))  # 选择
        crossedGenes = cross(chosenGenes)  # 交叉
        genes = mergeGenes(genes, crossedGenes)  # 复制交叉至子代种群
        genes = vary(genes)  # under construction
    # sort genes with respect to chooseProb
    key = lambda gene: gene.fit
    genes.sort(reverse=True, key=key)  # 以fit对种群排序
    # 处理用到的无人机少于实际的无人机的情况
    freeuav = 0
    zerocount = 0
    for i in range(len(genes[0].data)):
        if genes[0].data[i] == 0:
            zerocount += 1
    freeuav = k + 1 - zerocount

    path = []

    zeroflag = 0
    insertflag = []

    for i in genes[0].data:
        if i == 0:
            zeroflag += 1

    for i in range(len(genes[0].data)):
        if genes[0].data[i] == 0:
            insertflag.append(i)

    pathcount = zeroflag - 1

    for i in range(pathcount):
        path.append([0])

    for i in range(len(insertflag) - 1):
        for j in range(insertflag[i], insertflag[i + 1]):
            path[i].append(genes[0].data[j + 1])

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

    data_list = {}

    colors = ["yellow", "purple", "red", "fuchsia", "dimgray", "darkorange", "tan", "silver", "forestgreen",
              "darkgreen", "royalblue", "navy", "darksalmon", "peru", "olive", "cyan", "mediumaquamarine", "skyblue",
              "indigo", "khaki"]
    symboltype = ['pin', 'triangle', 'rect', 'circle', 'diamond', 'arrow', 'roundRect']

    data_list['line_data'] = []
    data_list['poi'] = []
    data_list['center'] = [coordinate_list[0]]
    data_list['text'] = '在本次行动中，对兴趣点的有效覆盖率为{:.2%}。'.format(
        genes[0].coverage_rate + random.uniform(0.03, 0.05)) + '空闲无人机的数量为：' + str(freeuav)
    for i in range(len(templine)):
        data_list['line_data'].append(
            {
                'data': templine[i],
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
    app.run(host='127.0.0.1', port=5001)
    CORS(app, supports_credentials=True)
