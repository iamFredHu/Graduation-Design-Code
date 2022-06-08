import math
import sys
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from data_preprocessing import *
from TSP_edges import *
from nx_draw import *



# m 无人机数量
# n POI数量
# nodelist POI编号
# D 距离矩阵
# Weight POI编号和权值构成的字典
# v 无人机飞行速度 m/s  72km/h = 20m/s
# omega 无人机转弯角速度 0.1rad/s = 5.7°/s
# t_max 无人机续航时间 s  90min = 5400s
def MRMinExpand(m, nodelist, D, Data, v, omega, t_max,e):
    n = len(D)
    path = [[] for _ in range(m)]  # 每一个无人机的路径
    T = [[0] for _ in range(m)] # 每一个无人机路径的飞行时间，累积计时器
    effective = [0 for _ in range(n)] # 标记POI是否被有效访问(在规定时间内访问)
    onTime = [0 for _ in range(n)] # 标记POI是否被准时访问
    visited = [0 for _ in range(n)] # 标记POI是否被访问
    time_initCheck(D, Data, v, e)

    P_0 = 0 # 起点（基站）
    nodelist.remove(P_0) # 去掉起点（基站）
    total_k = 0  # 最终实际无人机数量

    for k in range(m):
        Tr = [x * 60 for x in Data]  # Tr为各POI剩余访问时间,将分钟换成秒
        # 首先把最远的POI加入路径
        long = 0
        longest = 0
        if len(nodelist)==0:
            break
        for i in nodelist:
            if D[0][i]>long:
                long = D[0][i]
                longest = i
        path[k].append(longest)
        nodelist.remove(longest)
        if len(nodelist) == 0:
            total_k = k + 1
        t_f_longest = D[0][longest]/v
        T[k].append(t_f_longest)
        visited[longest] = 1
        if(T[k][-1]<=Data[longest]*60*(1+e)):
            effective[longest] = 1
        if(T[k][-1]<=Data[longest]*60):
            onTime[longest] = 1
        for i in range(1, n):
            Tr[i] = Tr[i] - t_f_longest  # 所有剩余访问时间变小

        while len(nodelist) and (P_0 not in path[k]):
            t_f = [0 for _ in range(n)] # 记录选择每一个POI的飞行时间
            t_f_r = [0 for _ in range(n)]  # 记录选择每一个POI且飞回起点的飞行时间
            p = 0 # 本轮待选点
            t_f_min = math.inf
            for i in nodelist:
                angle = 0
                # 飞行时间=距离时间+转弯时间
                if(len(path[k]) == 1):
                    angle = calculate_angle(D, 0, path[k][-1], i)
                else:
                    angle = calculate_angle(D,path[k][-2],path[k][-1],i)
                t_f[i] = D[path[k][-1]][i]/v + angle/omega
                angle_r = calculate_angle(D, path[k][-1], i, 0)
                t_r_i = D[i][0] / v + angle_r / omega  # 从i飞回起点的时间
                t_f_r[i] = t_f[i] + t_r_i


                #每次选当前剩余时间最短且能满足准时的
                if(T[k][-1]+t_f[i]<=Data[i]*60*(1+e)) and t_f[i]<t_f_min:
                    t_f_min = t_f[i]
                    p = i

            print("p:%d"%p)
            # 选择p会超过续航时间 或者 p==0 则返回基站
            if(T[k][-1]+t_f[p]+t_f_r[p]>t_max or p==0):
                path[k].append(P_0)
                if (len(path[k]) == 2): #（此时0已经被加到路径最后了）
                    angle = 180
                else:
                    angle = calculate_angle(D, path[k][-3], path[k][-2], 0)
                t_last = D[path[k][-2]][0] / v + angle / omega # 从最后一个POI回到起点的时间
                T[k].append(T[k][-1] + t_last) # 路径k最终用时，存于T[k]最后一项

            elif (p!=0):
                path[k].append(p)
                nodelist.remove(p)
                T[k].append(T[k][-1]+t_f[p])
                for i in range(1, n):
                    Tr[i] = Tr[i] - t_f[p]  # 所有剩余访问时间变小
                visited[p] = 1
                if (T[k][-1] <= Data[p] * 60*(1+e)):
                    effective[p] = 1
                if(T[k][-1]<=Data[p]*60):
                    onTime[p] = 1
            print("nodelist:")
            print(nodelist)
            if len(nodelist)== 0:
                total_k = k + 1

        path[k].insert(0, 0) # 将起点加到路径最前面
        print("path[%d]:" % k)
        print(path[k])
        # print("path[%d]路径总时间：%f秒 = %f分钟" %(k,T[k][-1],T[k][-1]/60))
        # print("--------------------------------------------")

    # 计算标准覆盖率
    coverage = 0
    for i in visited:
        coverage += i
    coverage_rate = coverage / (n - 1)

    #计算有效覆盖率
    effective_coverage = 0
    for i in effective:
        effective_coverage += i
    effective_coverage_rate = effective_coverage / (n - 1)
    # print("有效覆盖率：%f" % effective_coverage_rate)  # 即在POI规定时间内访问（允许超20%），超过时间就是无效访问

    # 计算准时率
    punctual = 0
    for i in onTime:
        punctual += i
    onTime_rate = punctual / (n - 1)

    print("标准覆盖率：%f  有效覆盖率：%f  准时率:%f" % (coverage_rate, effective_coverage_rate, onTime_rate))
    # # print("标准覆盖率：%f  准时率:%f" % (coverage_rate, onTime_rate))
    # print(path)

    print("无人机数量:%d" % total_k)

    return path, effective_coverage_rate, onTime_rate, total_k


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
    angle_B = math.degrees(math.acos((a ** 2 + c ** 2 - b ** 2) / (2 * a * c)))
    angle = 180 - angle_B
    return angle


if __name__ == '__main__':
    N = 100
    m = 4
    # path_length = 800
    omega = 5.7 # 无人机转弯角速度
    S = 50 # 面积S*S
    t_max = 10800  # 无人机续航时间，3h = 180min = 10800s
    # delay = 150  # 时延
    ts_min = 50 #最小的ts值，即最短的要求访问时间
    ts_max = 140 #最大的ts值，即最长的要求访问时间
    e = 0  # 容忍系数
    nodes = get_nodes(N,S,ts_min,ts_max)
    nodelist, coordinate, Data = get_parameters(nodes)
    nodelist_copy = list(nodelist)
    # nodelist.remove(0)
    # print(nodelist)
    Data = dict(zip(nodelist, Data))  # 将POI编号与数据组成dict
    print(Data)
    D = get_distance_matrix(nodes)
    D *= 1000 # 千米换成米
    path,effective_coverage_rate,onTime_rate = MRMinExpand(m,nodelist,D,Data,25,omega,t_max,e) # 此方法最后置空了nodelist
    print('path:', path)
    edges = get_edges(path)
    print(nodelist_copy)
    # nx_draw(nodelist_copy, coordinate, edges, 'WTSC.png')
