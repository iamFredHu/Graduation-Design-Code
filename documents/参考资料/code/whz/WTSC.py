import math
import sys
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from data_preprocessing import *
from TSP_edges import *
from nx_draw_old import *



# m 无人机数量
# n POI数量
# nodelist POI编号
# D 距离矩阵
# Weight POI编号和权值构成的字典
# v 无人机飞行速度 m/s  72km/h = 20m/s
# omega 无人机转弯角速度 0.1rad/s = 5.7°/s
# t_max 无人机续航时间 s  90min = 5400s



def WTSC(m, nodelist, D, Weight, v, omega, t_max,e):
    n = len(D)
    # print("--------")
    # print(n)
    # total_weight = 0
    # for w in range(n):
    #     total_weight += w
    time_initCheck(D, Weight, v, e)
    path = [[] for _ in range(m)]  # 每一个无人机的路径
    T = [[0] for _ in range(m)] # 每一个无人机路径的飞行时间
    T_c = [] # 每一条路径用的总时间
    effective = [0 for _ in range(n)] # 标记POI是否被有效访问(在规定时间内访问)
    onTime = [0 for _ in range(n)] # 标记POI是否被准时访问
    visited = [0 for _ in range(n)] # 标记POI是否被访问
    Gama = [] #超时系数

    P_0 = 0 # 起点（基站）
    nodelist.remove(P_0) # 去掉起点（基站）
    total_k = 0 # 最终实际无人机数量
    for k in range(m):
        while len(nodelist) and (P_0 not in path[k]):
            cost = [math.inf for _ in range(n)] # 记录选择每一个POI的cost
            t = [0 for _ in range(n)] # 记录选择每一个POI的飞行时间
            for i in nodelist:
                angle = 0
                if(len(path[k]) == 0): # 从起点出发，选择第一个POI
                    t[i] = D[0][i] / v
                else:
                    # 飞行时间=距离时间+转弯时间
                    if(len(path[k]) == 1):
                        angle = calculate_angle(D, 0, path[k][-1], i)
                    else:
                        angle = calculate_angle(D,path[k][-2],path[k][-1],i)
                    t[i] = D[path[k][-1]][i]/v + angle/omega

                # # 超时的就赋cost无穷大，不超时的正常计算cost
                if(T[k][-1]+t[i]>Weight[i]*60):
                    cost[i] = math.inf
                else:
                    a = 0.1
                    cost[i] = a * t[i] + (1-a)/Weight[i]
                # cost[i] = t[i]+Weight[i]
                # 转弯限制相关代码
                # if(angle>120):
                #     cost[i] = math.inf
                # cost[i] =  t[i] / Weight[i]
            # print(cost)
            p = cost.index(min(cost)) # 代价最小的POI编号

            # 转弯限制相关代码
            # if(p==P_0):
            #     path[k].append(P_0)
            #     break

            #计算t_last_tmp,即最后返回基站的时间
            if (len(path[k]) == 0):
                angle = 180
            else:
                angle = calculate_angle(D, path[k][-1], p, 0)
            t_last_tmp = D[p][0] / v + angle / omega  # 从最后一个POI回到起点的时间

            if(T[k][-1]+t[p]+t_last_tmp < t_max):
                T[k].append(T[k][-1]+t[p])
                path[k].append(p)
                nodelist.remove(p)
                visited[p] = 1
                if(T[k][-1] < Weight[p]*60*(1+e)):
                    effective[p] = 1
                if(T[k][-1] < Weight[p]*60):
                    onTime[p] = 1
                else:
                    # 超时系数
                    gama = (T[k][-1] - Weight[p] * 60) / (Weight[p] * 60)
                    Gama.append(gama)
                    # print("超时系数：%f" % gama)
            else:
                # angle = calculate_angle(D, path[k][-2], path[k][-1], 0)
                if (len(path[k]) == 1):
                    angle = 180
                else:
                    angle = calculate_angle(D, path[k][-2], path[k][-1], 0)
                t_last = D[path[k][-1]][0] / v + angle / omega # 从最后一个POI回到起点的时间
                path[k].append(P_0)
                T[k].append(T[k][-1]+t_last)

                # T_fk = T_fk-t[p]+t_last
                # T_c.append(T_fk)

            if len(nodelist)== 0:
                total_k = k + 1


        # #计算每条路径总时间，存于T_c
        # T_ck = 0
        # for i in T[k]:
        #     T_ck += i
        o = 1 # 操作员数量
        # T_ck += 600 * math.ceil(k/o) # 一架无人机起飞时间10min=600s
        T_c.append(T[k][-1]+ 600 * math.ceil(k/o))
        path[k].insert(0, 0) # 将起点加到路径最前面
        # if path[k][-1] != P_0:
        #     path[k].append(P_0)
        # print("path[%d]:" % k)
        # print(path[k])

    T_final = max(T_c)
    print("每条路径总时间：----------------------")
    print([x/60 for x in T_c])
    # coverage_rate = calculate_rate(path, Weight)
    print("最终用时：%f秒" % T_final)


    standard_coverage = 0
    for i in visited:
        standard_coverage += i
    standard_coverage_rate = standard_coverage/(n-1)
    print("标准覆盖率：%f" % standard_coverage_rate)

    effective_coverage = 0
    for i in effective:
        effective_coverage += i
    effective_coverage_rate = effective_coverage/(n-1)
    print("有效覆盖率：%f" % effective_coverage_rate) # 即在POI规定时间内访问（允许超20%），超过时间就是无效访问

    onTime_coverage = 0
    for i in onTime:
        onTime_coverage += i
    onTime_rate = onTime_coverage/(n-1)
    print("准时率：%f" % onTime_rate)
    # print("超时系数均值：%f"%np.average(Gama))

    print("无人机数量:%d" % total_k)

    return path,effective_coverage_rate,onTime_rate,total_k


# 初始化数据，检查时间是否合理
def time_initCheck(D, Data, v,e):
    n = len(D) # POI个数+1
    print("--------")
    print(n)
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


# 计算转弯角度
def calculate_angle(D, front, current, x):
    a = D[current][x]
    c = D[front][current]
    b = D[front][x]
    try:
        angle_B = math.degrees(math.acos((a ** 2 + c ** 2 - b ** 2) / (2 * a * c)))
    except ValueError:  # acos=-1的情况，角B为180
        angle_B = 180
    angle = 180 - angle_B
    return angle

#计算覆盖率
def calculate_rate(path, Weight):
    weight_total = 0
    for i in range(len(Weight)):
        weight_total += Weight[i]
    print("所有POI权重和：%f" % weight_total)

    weight_sum = 0
    for i in range(len(path)):
        for j in range(len(path[i])):
            weight_sum += Weight[path[i][j]]
    print("覆盖的权重之和为：%f" % weight_sum)

    coverage_rate = weight_sum/weight_total
    print("带权覆盖率为：%f" % coverage_rate)
    return coverage_rate



if __name__ == '__main__':
    N = 100
    m = 4
    # path_length = 800
    omega = 5.7 # 无人机转弯角速度
    S = 50 # 面积S*S
    t_max = 9000  # 无人机续航时间，3h = 180min = 10800s
    # delay = 150  # 时延
    e = 0  # 容忍系数
    ts_min = 50 #最小的ts值，即最短的要求访问时间
    ts_max = 140 #最大的ts值，即最长的要求访问时间
    nodes = get_nodes(N,S,ts_min,ts_max)
    nodelist, coordinate, Data = get_parameters(nodes)
    nodelist_copy = list(nodelist)
    # nodelist.remove(0)
    # print(nodelist)
    Data = dict(zip(nodelist, Data))  # 将POI编号与数据组成dict
    print(Data)
    D = get_distance_matrix(nodes)
    D *= 1000 # 千米换成米
    path,effective_coverage_rate,onTime_rate,k = WTSC(m,nodelist,D,Data,25,omega,t_max,e) # 此方法最后置空了nodelist
    print('path:', path)
    edges = get_edges(path)
    print(nodelist_copy)
    nx_draw_old(nodelist_copy, coordinate, edges, 'WTSC.png')


