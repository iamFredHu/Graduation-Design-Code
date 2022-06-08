import math
import sys
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from data_preprocessing import *
from TSP_edges import *
from nx_draw import *

# Data为每个POI返回时间限制
def MRMinExpand(n, D, t_max, Data, speed,omega):
    Q = 0.0
    N = len(D) # POI个数
    S = [0.0 for _ in range(n)] #每条路径长度
    path = [[0] for _ in range(n)] # 每一个移动传感器的路径
    visited = [0 for _ in range(N)] # 标记POI是否被访问
    # visited[0] = 1
    effective = [0 for _ in range(N)] # 标记POI是否被有效访问(在规定时间内访问)
    onTime = [0 for _ in range(N)] # 标记POI是否被准时访问
    tr = [t_max] * n # 变成n个列表，tr代表续航时间
    T = [[0] for _ in range(m)]  # 每一个无人机路径的飞行时间
    path[0].append(70)
    for i in range(n): # n为移动传感器个数
        T = 0  # 已花费时间
        while True:
            delta = -float('inf')
            candi_v = -1
            t_f = [0 for _ in range(N)]  # 记录选择每一个POI的飞行时间
            for v in range(1, N): # 对每一个POI（除了起点），找具有最大剩余时间的点
                if visited[v] == 0:
                    # 计算飞到该POI的时间
                    if (len(path[i]) == 1):  # 从起点出发，选择第一个POI
                        t_f[v] = D[0][v] / speed
                    else:
                        angle = calculate_angle(D,path[i][-2],path[i][-1],v)
                        t_f[v] = D[path[i][-1]][v]/speed + angle/omega
                    # 在 剩余续航时间 与 每个POI返回时间限制 选较小的，再减去返回起点的时间，看还剩多少
                    tp_delta = min(tr[i] - t_f[v], Data[v]*60) - D[v][0]/speed # 访问该POI后再回到起点，剩余的时间
                    # tp_delta = min(tr[i] - t_f[v], 3000) - D[v][0] / speed
                    if tp_delta > delta:
                        delta = tp_delta
                        candi_v = v
            if delta < 0: # 剩余时间为负
                path[i].append(0) # 返回基站
                Ts = tr[i] - t_f[candi_v]-D[candi_v][0]/speed # 剩余续航时间（没用完的）
                if(Ts > 0):
                    closest = 0
                    min_distance = math.inf
                    for j in range(1,N):
                        if visited[j] != 1 and D[0][j] < min_distance:
                            closest = j
                    t_closest = 2 * D[0][closest] / speed + 180 / omega
                    if closest!=0 and t_closest <= Ts:
                        path[i].append(closest)
                        visited[closest] = 1
                        T += D[0][closest]
                        if (T < Data[closest] * 60 * 1.2):
                            effective[closest] = 1
                        if (T < Data[closest] * 60):
                            onTime[closest] = 1
                break
            else:
                # 取 到达该POI后剩余续航时间 与 该POI的返回时间限制 较小者，作为剩余续航时间
                tr[i] = min(tr[i] - t_f[candi_v], Data[candi_v]*60)
                # tr[i] = min(tr[i] - t_f[candi_v], 3000)
                path[i].append(candi_v)
                visited[candi_v] = 1
                T += t_f[candi_v]
                if(T < Data[candi_v]*60*1.2):
                    effective[candi_v] = 1
                if(T < Data[candi_v]*60):
                    onTime[candi_v] = 1
        for j in range(len(path[i]) - 1):
            S[i] += D[path[i][j]][path[i][j + 1]] # 每条路径长度

    standard_coverage = 0
    for i in visited:
        standard_coverage += i
    standard_coverage_rate = standard_coverage/(N-1)
    print("标准覆盖率：%f" % standard_coverage_rate)

    effective_coverage = 0
    for i in effective:
        effective_coverage += i
    effective_coverage_rate = effective_coverage/(N-1)
    print("有效覆盖率：%f" % effective_coverage_rate) # 即在POI规定时间内访问（允许超20%），超过时间就是无效访问

    onTime_coverage = 0
    for i in onTime:
        onTime_coverage += i
    onTime_rate = onTime_coverage/(N-1)
    print("准时率：%f" % onTime_rate)

    return path, effective_coverage_rate,onTime_rate


# 计算转弯角度
def calculate_angle(D, front, current, x):
    a = D[current][x]
    c = D[front][current]
    b = D[front][x]
    angle_B = math.degrees(math.acos((a ** 2 + c ** 2 - b ** 2) / (2 * a * c)))
    angle = 180 - angle_B
    return angle


if __name__ == '__main__':
    m = 5
    t_max = 10800 # 续航时间
    omega = 5.7 # 无人机转弯角速度
    v = 25 # 速度
    S = 50 # 面积S*S
    # delay = 4150  # 时延，这里将所有POI返回时间限制设为一致
    nodes = get_nodes(100,S,50,140)
    nodelist, coordinate, Data = get_parameters(nodes)
    Data = dict(zip(nodelist, Data))  # 将POI编号与数据组成dict
    D = get_distance_matrix(nodes)
    print(D)
    D *= 1000 # 千米换成米
    path, effective_coverage_rate,onTime_rate = MRMinExpand(m, D, t_max, Data,v,omega)
    print('path:', path)
    edges = get_edges(path)
    nx_draw(nodelist, coordinate, edges, 'G-MSCR.png')


