import math
import sys
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from data_preprocessing import *
from TSP_edges import *
from nx_draw import *
from nx_draw_old import *

# 改进：如果是最后一架无人机，在要返回基站时，再检查有没有POI未被访问，如果有，去把那些POI访问了，实现100%全覆盖。


# m 无人机数量
# n POI数量
# nodelist POI编号
# D 距离矩阵
# Data POI剩余访问时间（时间敏感性）
# v 无人机飞行速度 m/s  90km/h = 25m/s
# omega 无人机转弯角速度 0.1rad/s = 5.7°/s
# t_max 无人机续航时间  180min = 10800s  经计算，续航时间不能低于1.58h（否则无法到达最远再回来）
# tolerance POI的允许超时时间（min），即初始剩余访问时间的20%
def my_method(m, nodelist, D, Data, v, omega, t_max,e):
    n = len(D)

    tolerance = time_initCheck(D, Data, v,e)

    path = [[] for _ in range(m)]  # 每一个无人机的路径
    T = [[0] for _ in range(m)] # 每一个无人机路径的累积飞行时间

    visited = [0 for _ in range(n)] # 标记POI是否被访问
    effective = [0 for _ in range(n)]  # 标记POI是否被有效访问(在允许时间内访问)
    onTime = [0 for _ in range(n)] # 标记POI是否被准时访问

    P_0 = 0 # 起点（基站）
    nodelist.remove(P_0) # 去掉起点（基站）
    for k in range(m):
        # T_remain = t_max  # 无人机剩余的续航时间
        Tr = [x*60 for x in Data] # Tr为各POI剩余访问时间,将分钟换成秒

        while len(nodelist) and (P_0 not in path[k]):
            cost = [math.inf for _ in range(n)] # 记录选择每一个POI的cost
            t_f = [0 for _ in range(n)] # 记录选择每一个POI的飞行时间
            t_f_r = [0 for _ in range(n)] # 记录选择每一个POI且飞回起点的飞行时间
            for i in nodelist: # 对nodelist里现有的每一个POI
                # 判断该poi是否可达，需要计算该poi的t_f和t_f_r
                angle = 0
                if(len(path[k]) == 0): # 从起点出发，选择第一个POI
                    t_f[i] = D[0][i] / v
                    t_f_r[i] = 2*t_f[i] + 180/omega
                else:
                    # 飞行时间=距离时间+转弯时间
                    if(len(path[k]) == 1):
                        angle = calculate_angle(D, 0, path[k][-1], i)
                    else:
                        angle = calculate_angle(D,path[k][-2],path[k][-1],i)
                    t_f[i] = D[path[k][-1]][i]/v + angle/omega
                    angle_r = calculate_angle(D,path[k][-1],i,0)
                    t_r_i = D[i][0]/v + angle_r/omega # 从i飞回起点的时间
                    t_f_r[i] = t_f[i] + t_r_i

                # 判断该poi是否可达
                T_remain = t_max - T[k][-1] # 剩余的续航时间
                tr_remain = Tr[i] - t_f[i] # 飞过去后，该POI的剩余访问时间
                # tr_remain = Tr[i] - T[k][-1] -t_f[i] # 飞过去后，该POI的剩余访问时间

                if tr_remain<0 and math.fabs(tr_remain)>tolerance[i]*60:
                # if tr_remain < 0:
                    cost[i] = math.inf  # 该POI已经死了，不可达，代价置为无穷大
                else: # 该POI还活着
                    if t_f_r[i] > T_remain: # 剩余续航时间不足以选该POI
                        cost[i] = math.inf # 不可达，代价置为无穷大
                    else:
                        # 计算该poi的cost
                        rou = 2
                        fai = T[k][-1] / t_max
                        # cost[i] =  t_f[i] +Tr[i]**(fai) + ((t_f_r[i] - t_f[i]) / fai) ** fai
                        cost[i] = t_f[i] + Tr[i] ** (fai)
                        # cost[i] = t_f[i]


            # print(cost)
            p = cost.index(min(cost)) # 代价最小的POI编号 (如果全都是inf，会返回0，即回到起点)

            path[k].append(p)
            print("path[%d]:" % k)
            print(path[k])

            if p != 0:
                nodelist.remove(p)
                visited[p] = 1
                T[k].append(T[k][-1]+t_f[p]) # 访问新的poi后，计算当前总耗时，存于T[k]最后面
                for i in range(1,n):
                    Tr[i] = Tr[i] - t_f[p] # 所有剩余访问时间变小
                if(T[k][-1] < Data[p]*60*(1+e)):
                    effective[p] = 1
                if Tr[p]>=0:
                # if Tr[p] - T[k][-1]>=0:
                    onTime[p] = 1 #剩余访问时间大于0，代表被准时访问。如果小于0，就是在20%内的不准时访问

            else: # 代价最小的为起点，则返回起点（代价全inf情况）
                t_last = 0
                if (len(path[k]) >= 2):
                    if (len(path[k]) == 2): #（此时0已经被加到路径最后了）
                        angle = 180
                    else:
                        angle = calculate_angle(D, path[k][-3], path[k][-2], 0)
                    t_last = D[path[k][-2]][0] / v + angle / omega # 从最后一个POI回到起点的时间
                T[k].append(T[k][-1] + t_last) # 路径k最终用时，存于T[k]最后一项




        path[k].insert(0, 0) # 将起点加到路径最前面
        print("path[%d]:" % k)
        print(path[k])
        print("path[%d]路径总时间：%f秒 = %f分钟" %(k,T[k][-1],T[k][-1]/60))
        print("--------------------------------------------")

    last_coverage(m,visited,D,path,T,v,t_max,Data,effective,e)
    #计算标准覆盖率
    coverage = 0
    for i in visited:
        coverage += i
    coverage_rate = coverage/(n-1)

    #计算有效覆盖率
    effective_coverage = 0
    for i in effective:
        effective_coverage += i
    effective_coverage_rate = effective_coverage / (n - 1)
    print("有效覆盖率：%f" % effective_coverage_rate)  # 即在POI规定时间内访问（允许超20%），超过时间就是无效访问

    #计算准时率
    punctual = 0
    for i in onTime:
        punctual += i
    onTime_rate = punctual/(n-1)

    print("标准覆盖率：%f  有效覆盖率：%f  准时率:%f" % (coverage_rate,effective_coverage_rate,onTime_rate))
    print(path)

    return path,effective_coverage_rate,onTime_rate






# # 最后一架无人机将所有未被覆盖的POI都覆盖，尽管已经超时
#未被覆盖的，离谁近就谁覆盖
def last_coverage(m,visited,D,path,T,v,t_max,Data,effective,e):
    Gama = []
    n = len(visited)
    for i in range(1,n):
        if visited[i] == 0:
            dis_ik = math.inf
            choose_k = m+1
            for k in range(m):
                if(T[k][-2]+D[i][path[k][-2]]/v+ D[i][0]/v <= t_max):
                    if D[i][path[k][-2]]<dis_ik:
                        dis_ik = D[i][path[k][-2]]
                        choose_k = k
            if(choose_k>=m):
                break
            path[choose_k].insert(-1,i)
            visited[i] = 1
            # print("更新后的path[%d]:" % (choose_k))
            # print(path[choose_k])
            t_f = dis_ik/v
            T[choose_k][-1] = T[choose_k][-2]+t_f
            if (T[choose_k][-1] < Data[i] * 60 * (1+e)):
                effective[i] = 1
            # #超时系数
            # gama = (T[choose_k][-1]-Data[i] * 60)/(Data[i] * 60)
            # print("超时系数：%f"%gama)
            # Gama.append(gama)
            T[choose_k].append(T[choose_k][-1]+D[i][0]/v)
            # print("更新后的path[%d]总时间:%f" % (choose_k,T[choose_k][-1]/60))
    # print("超时系数均值：%f"%np.average(Gama))




# 计算转弯角度
def calculate_angle(D, front, current, x):
    a = D[current][x]
    c = D[front][current]
    b = D[front][x]
    try:
        angle_B = math.degrees(math.acos((a ** 2 + c ** 2 - b ** 2) / (2 * a * c)))
    except ValueError: # acos=-1的情况，角B为180
        angle_B = 180
    angle = 180 - angle_B
    return angle

# 初始化数据，检查时间是否合理
def time_initCheck(D, Data, v,e):
    n = len(D) # POI个数+1
    # print("--------")
    # print(n)
    tolerance = [0] # 装POI的允许超时时间（min），即初始剩余访问时间的20%
    for i in range(1,n):
        t = D[0][i] / v # 从起点直接飞过去的时间,单位：s
        t = t/60 # 秒换成分钟
        tr_i = Data[i]
        if(tr_i < t): # 剩余访问时间 比 直飞距离时间 小，是无法访问的，需重新设置剩余访问时间
            Data[i] = np.random.randint(t, 120 + 1)
        tolerance_i = Data[i] * e
        tolerance.append(tolerance_i)
    return tolerance










if __name__ == '__main__':
    N = 100
    m = 5
    v = 25 # 无人机飞行速度，25m/s = 90km/h
    t_max = 10800 # 无人机续航时间，3h = 180min = 10800s
    # t_max = 7200 # 2h
    # t_max = 9000 # 2.5h
    # t_max = 14400 #4h
    S = 50 # 面积S*S
    d = 1
    R = 2# R >= [（根号2）/2] * d ,必须满足这个条件，这样一个圆盘才能包住一个网格


    omega = 5.7 # 无人机转弯角速度
    e = 0 #容忍系数
    ts_min = 50 #最小的ts值，即最短的要求访问时间
    ts_max = 140 #最大的ts值，即最长的要求访问时间
    nodes = get_nodes(N,S,ts_min,ts_max)
    nodelist, coordinate, Data = get_parameters(nodes)

    nodelist_copy = list(nodelist)
    pos = dict(zip(nodelist, coordinate))  # POI编号和坐标,包含基站

    # circle_cover(S, N, d, R, pos, Data)

    Data = dict(zip(nodelist, Data))  # 将POI编号与数据组成dict,数据为POI的剩余访问时间，单位为min

    D = get_distance_matrix(nodes)
    D *= 1000 # 千米换成米

    path, coverage_rate, onTime_rate = my_method(m, nodelist, D, Data, v, omega, t_max,e)
    # path,coverage_rate,onTime_rate,center_points,final_set_label_copy = my_method(m,nodelist,D,Data,v,omega,t_max,e,S,N,d,R,pos) # 此方法最后置空了nodelist
    edges = get_edges(path)
    print(edges)
    nx_draw_old(nodelist_copy, coordinate, edges, 'whz.png')


    # nx_draw(nodelist_copy, coordinate, edges,center_points,final_set_label_copy,R)

