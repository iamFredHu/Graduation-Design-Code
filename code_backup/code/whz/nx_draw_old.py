import networkx as nx
import matplotlib.pyplot as plt
from data_preprocessing import *

def nx_draw_old(nodelist, coordinate, edges, name, Label = False):
    G = nx.Graph()
    pos = dict(zip(nodelist, coordinate))
    labels = dict(zip(nodelist, nodelist))
    nx.draw_networkx_nodes(G, pos, nodelist, node_size=5, node_color='r')
    # nx.draw_networkx_nodes(G, {0: [0, 0]}, {0: 0}, node_size=10, node_color='g')
    # print(edges[0])
    print("aaaaaaaaaaa")

    nx.draw_networkx_edges(G, pos, edges[0],edge_color='blue')
    nx.draw_networkx_edges(G, pos, edges[1],edge_color='purple')
    nx.draw_networkx_edges(G, pos, edges[2],edge_color='green')
    nx.draw_networkx_edges(G, pos, edges[3],edge_color='black')
    nx.draw_networkx_edges(G, pos, edges[4],edge_color='orange')
    #nx.draw_networkx_edges(G, pos, edges[5],edge_color='red')
    #nx.draw_networkx_edges(G, pos, edges[6],edge_color='purple')
    #nx.draw_networkx_edges(G, pos, edges[7],edge_color='pink')

    if Label:
        nx.draw_networkx_labels(G, pos, labels, font_size=5)

    # plt.title()默认是显示英文,加以下两行可显示中文
    # 解决中文显示问题
    # plt.rcParams['font.sans-serif'] = ['SimHei']
    # plt.rcParams['axes.unicode_minus'] = False
    n = len(nodelist)-1
    plt.title('n=%d' % n)
    plt.show()
    # plt.savefig(name)


if __name__ == '__main__':
    N = 50
    m = 10
    v = 25 # 无人机飞行速度，25m/s = 90km/h
    t_max = 10800 # 无人机续航时间，3h = 180min = 10800s
    S = 50 # 面积S*S
    d = 5
    R = 5

    omega = 5.7 # 无人机转弯角速度
    e = 0 #容忍系数
    ts_min = 60 #最小的ts值，即最短的要求访问时间
    ts_max = 150 #最大的ts值，即最长的要求访问时间
    nodes = get_nodes(N,S,ts_min,ts_max)
    nodelist, coordinate, Data = get_parameters(nodes)
    nx_draw(nodelist, coordinate, [], 'whz.png')
