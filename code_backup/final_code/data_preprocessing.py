# encoding: utf-8
import sys
import math
import numpy as np
import pandas as pd



## First reading the VRP from the input ##


def readinput():
    try:
        line = input().strip()
        while line == '' or line.startswith('#'):
            line = input().strip()
        return line
    except EOFError:
        return None
        
def distance(n1, n2):
    dx = n2['posX'] - n1['posX']
    dy = n2['posY'] - n1['posY']
    return math.sqrt(dx * dx + dy * dy)

# def get_nodes():
#     vrp = {}
#     vrp['nodes'] = []
#     line = readinput()
#     print("aaaaaaaa")
#     if line is None:
#         print(sys.stderr, 'Empty input!')
#         exit(1)
#     while line is not None:
#         inputs = line.split()
#         if len(inputs) < 4:
#             print(sys.stderr, 'Invalid input: too few arguments for a node!')
#             exit(1)
#         node = {
#             'label': int(float(inputs[0])), 'data.txt': float(
#                 inputs[1]), 'posX': float(
#                 inputs[2]), 'posY': float(
#                     inputs[3])}
#         # Validating demand neither negative nor zero
#         if node['data.txt'] < 0:
#             print(sys.stderr, 'Invalid input: the data.txt if the node %s is negative!' % node[
#                 'label'])
#             exit(1)
#         vrp['nodes'].append(node)
#         line = readinput()
#
#     # Validating no such nodes
#     if len(vrp['nodes']) == 0:
#         print(sys.stderr, 'Invalid input: no such nodes!')
#         exit(1)
#
#     return vrp

# 新get_nodes N为POI数量，S为面积S*S
def get_nodes(N,S,ts_min,ts_max):
    s = 'C:\\Users\\hucon\\Desktop\\code\\data\\'
    distribution = 'Uniform'
    s = s + distribution + '-' + str(N) + '-'+str(S)+'-'+str(ts_min)+'-'+str(ts_max)+'.txt'
    nodes = pd.read_table(s, sep='\t', header=None)  # 读入txt文件，分隔符为\t
    nodes.columns = ['label']
    nodes['data'] = None
    nodes['posX'] = None
    nodes['posY'] = None
    nodes['supply'] = None
    for j in range(len(nodes)):  # 遍历每一行
        coordinate = nodes['label'][j].split()  # 分开第i行，x列的数据。split()默认是以空格等符号来分割，返回一个列表
        nodes['label'][j] = int(float(coordinate[0]))  # 分割形成的列表第一个数据给label列
        nodes['data'][j] = float(coordinate[1])  # 分割形成的列表第二个数据给data列
        nodes['posX'][j] = float(coordinate[2])
        nodes['posY'][j] = float(coordinate[3])
        nodes['supply'][j] = float(coordinate[4])
    return nodes


# def get_distance_matrix(vrp):
#     N = len(vrp['nodes'])
#     D = np.zeros([N, N], dtype = float)
#     for i in range(N):
#         for j in range(N):
#             # num_i = vrp['nodes'][i]['label']
#             # num_j = vrp['nodes'][j]['label']
#             pi = vrp['nodes'][i]
#             pj = vrp['nodes'][j]
#             D[i][j] = D[j][i] = distance(pi, pj)
#     return D

# 新
def get_distance_matrix(nodes):
    N = len(nodes)
    D = np.zeros([N, N], dtype = float)
    for i in range(N):
        for j in range(N):
            i_x = float(nodes['posX'][i])
            j_x = float(nodes['posX'][j])
            i_y = float(nodes['posY'][i])
            j_y = float(nodes['posY'][j])
            D[i][j] = D[j][i] = math.sqrt((i_x - j_x) ** 2 + (i_y - j_y) ** 2)
    return D

# def get_parameters(vrp):
#     N = len(vrp['nodes'])
#     nodelist = []
#     coordinate = []
#     data = []
#     for i in range(N):
#         nodelist.append(vrp['nodes'][i]['label'])
#         coordinate.append((vrp['nodes'][i]['posX'], vrp['nodes'][i]['posY']))
#         data.append(vrp['nodes'][i]['data.txt'])
#     return nodelist, coordinate, data


# (新)把序号、坐标、数据分开，返回3个list
def get_parameters(nodes):
    N = len(nodes)
    nodelist = []
    coordinate = []
    data = []
    supply = []
    for i in range(N):
        nodelist.append(nodes['label'][i])
        coordinate.append((nodes['posX'][i], nodes['posY'][i]))
        data.append(nodes['data'][i])
        supply.append(nodes['supply'][i])
    return nodelist, coordinate, data, supply





