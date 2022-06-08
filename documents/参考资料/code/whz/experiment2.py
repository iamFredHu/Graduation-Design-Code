from multiMst import *
from MR_MinExpand import *
from G_MSCR import *
from data_generation import *
import numpy as np
import pandas as pd
from matplotlib import pyplot
import matplotlib.pyplot as plt
from whz import *
from WTSC import *


if __name__ == '__main__':
    # N = 100
    # m = 5
    # v = 25  # 无人机飞行速度，25m/s = 90km/h
    # t_max = 10800  # 无人机续航时间，3h = 180min = 10800min
    # omega = 5.7  # 无人机转弯角速度
    # S = 50 # 面积 S*S
    #
    #
    # x = []
    # y_coverage_my = []
    # y_onTime_my = []
    #
    # y_coverage_WTSC = []
    # y_onTime_WTSC = []
    #
    # y_coverage_GMSCR = []
    # y_onTime_GMSCR = []
    #
    # repeat_times = 50
    #
    # N_step = 25
    # for i in range(1, 17): # 对于每一个x值区间
    #     N = i * N_step
    #     effective_coverage_rate_my = 0.0
    #     effective_coverage_rate_WTSC = 0.0
    #     effective_coverage_rate_GMSCR = 0.0
    #     onTime_rate_my = 0.0
    #     onTime_rate_WTSC = 0.0
    #     onTime_rate_GMSCR = 0.0
    #     for _ in range(repeat_times): # 每一个x值对应的数据是跑repeat_times次出来的
    #         data_generation(N, S)
    #         nodes = get_nodes(N,S)
    #         nodelist, coordinate, Data = get_parameters(nodes)
    #         nodelist_copy = list(nodelist)
    #         D = get_distance_matrix(nodes)
    #         D *= 1000  # 千米换成米
    #         # 运行算法
    #         path_my, effective_coverage_rate_my_tmp, onTime_rate_my_tmp = my_method(m, nodelist, D, Data, v, omega, t_max)  # 此方法最后置空了nodelist
    #         path_WTSC,effective_coverage_rate_WTSC_tmp, onTime_rate_WTSC_tmp = WTSC(m, nodelist_copy, D, Data, v, omega, t_max)
    #         path_GMSCR,effective_coverage_rate_GMSCR_tmp,onTime_rate_GMSCR_tmp = G_MSCR(m, D, t_max, Data,v,omega)
    #
    #         # 结果取平均
    #         effective_coverage_rate_my += effective_coverage_rate_my_tmp/repeat_times
    #         onTime_rate_my += onTime_rate_my_tmp/repeat_times
    #
    #         effective_coverage_rate_WTSC += effective_coverage_rate_WTSC_tmp/repeat_times
    #         onTime_rate_WTSC += onTime_rate_WTSC_tmp/repeat_times
    #
    #         effective_coverage_rate_GMSCR += effective_coverage_rate_GMSCR_tmp/repeat_times
    #         onTime_rate_GMSCR += onTime_rate_GMSCR_tmp/repeat_times
    #
    #
    #     x.append(N)
    #     y_coverage_my.append(effective_coverage_rate_my)
    #     y_onTime_my.append(onTime_rate_my)
    #     y_coverage_WTSC.append(effective_coverage_rate_WTSC)
    #     y_onTime_WTSC.append(onTime_rate_WTSC)
    #     y_coverage_GMSCR.append(effective_coverage_rate_GMSCR)
    #     y_onTime_GMSCR.append(onTime_rate_GMSCR)
    #
    #
    # print("x=",x)
    # print("y_coverage_my=",y_coverage_my)
    # print("y_onTime_my=",y_onTime_my)
    # print("y_coverage_WTSC=",y_coverage_WTSC)
    # print("y_onTime_WTSC=",y_onTime_WTSC)
    # print("y_coverage_GMSCR=",y_coverage_GMSCR)
    # print("y_onTime_GMSCR=",y_onTime_GMSCR)


    x = [25, 50, 75, 100, 125, 150, 175, 200, 225, 250, 275, 300, 325, 350, 375, 400]
    y_coverage_my = [1.000, 1.000, 1.000, 0.999, 0.997, 0.982, 0.972, 0.949, 0.925, 0.911, 0.882, 0.868, 0.844, 0.827, 0.810, 0.796]
    y_onTime_my = [0.926, 0.919, 0.917, 0.919, 0.913, 0.900, 0.897, 0.877, 0.856, 0.848, 0.819, 0.807, 0.784, 0.771, 0.757, 0.745]
    y_coverage_WTSC = [0.748, 0.700, 0.718, 0.710, 0.679, 0.662, 0.676, 0.673, 0.664, 0.651, 0.650, 0.649, 0.656, 0.659, 0.656, 0.645]
    y_onTime_WTSC = [0.665, 0.606, 0.620, 0.605, 0.573, 0.563, 0.579, 0.573, 0.554, 0.543, 0.540, 0.541, 0.552, 0.556, 0.548, 0.537]
    y_coverage_GMSCR = [0.782, 0.751, 0.732, 0.687, 0.639, 0.585, 0.547, 0.518, 0.494, 0.464, 0.446, 0.427, 0.406, 0.395, 0.381, 0.362]
    y_onTime_GMSCR = [0.689, 0.647, 0.623, 0.588, 0.541, 0.497, 0.468, 0.437, 0.414, 0.392, 0.371, 0.363, 0.342, 0.332, 0.319, 0.303]

    # plt.figure(figsize=(12, 4.5))
    # plt.subplot(121)
    plt.xlim(25, 400)
    plt.ylim(0, 1)  # 限定纵轴的范围
    # plt.plot(x, y_coverage_my, linewidth=1, marker='o', ms=5, color = '#FF7F0E',label='GCS')
    # plt.plot(x, y_coverage_WTSC, linewidth=1, marker='x', ms=5, color = '#1F77B4',label='WTSC')
    # plt.plot(x, y_coverage_GMSCR, linewidth=1, marker='*', ms=5, color='#2CA02C',label='G-MSCR')
    # plt.legend()  # 让图例生效
    # # plt.xticks(x, names, rotation=1)
    # plt.margins(0)
    # plt.subplots_adjust(bottom=0.10)
    # plt.xlabel('Number of POI')  # X轴标签
    # plt.ylabel("effective coverage rate")  # Y轴标签
    #
    # plt.subplot(122)
    # plt.xlim(25, 400)
    # plt.ylim(0, 1)  # 限定纵轴的范围
    # plt.plot(x, y_onTime_my, linewidth=1, marker='o', ms=5, color = '#FF7F0E',linestyle = '--',label='GCS')
    # plt.plot(x, y_onTime_WTSC, linewidth=1, marker='x', ms=5, color = '#1F77B4',linestyle = '--',label='WTSC')
    # plt.plot(x, y_onTime_GMSCR, linewidth=1, marker='*', ms=5, color='#2CA02C',linestyle = '--',label='G-MSCR')
    # plt.legend()  # 让图例生效
    # # plt.xticks(x, names, rotation=1)
    # plt.margins(0)
    # plt.subplots_adjust(bottom=0.10)
    # plt.xlabel('Number of POI')  # X轴标签
    # plt.ylabel("on time rate")  # Y轴标签


    # 两率合在一起显示
    plt.plot(x, y_coverage_my, linewidth=1, marker='o', ms=5, color = '#FF7F0E',label='GCS-effective coverage rate')
    plt.plot(x, y_onTime_my, linewidth=1, marker='o', ms=5, color = '#FF7F0E',linestyle = '--',label='GCS-on time rate')
    plt.plot(x, y_coverage_WTSC, linewidth=1, marker='x', ms=5, color = '#1F77B4',label='WTSC-effective coverage rate')
    plt.plot(x, y_onTime_WTSC, linewidth=1, marker='x', ms=5, color = '#1F77B4',linestyle = '--',label='WTSC-on time rate')
    plt.plot(x, y_coverage_GMSCR, linewidth=1, marker='*', ms=5, color='#2CA02C',label='G-MSCR-effective coverage rate')
    plt.plot(x, y_onTime_GMSCR, linewidth=1, marker='*', ms=5, color='#2CA02C',linestyle = '--',label='G-MSCR-on time rate')
    plt.legend()  # 让图例生效
    plt.margins(0)
    plt.subplots_adjust(bottom=0.10)
    plt.xlabel('Number of POI')  # X轴标签
    plt.ylabel("effective coverage rate , on time rate")  # Y轴标签


    # pyplot.yticks([0.750,0.800,0.850])
    s = "./pic/"
    plt.savefig(s+'e2-UAV' + '-' + 'N-2'  + '.pdf', dpi=1000, format='pdf')
    plot_data = np.vstack((x, y_coverage_my,y_coverage_WTSC,y_coverage_GMSCR,y_onTime_my, y_onTime_WTSC,y_onTime_GMSCR))
    # np.savetxt(s+'e2-UAV' + '-' + 'N' + '.txt', plot_data, fmt='%.3f', delimiter=",")



# Performance varying with the number of mobile sensors
# N = 500
# path_length = 300
# delay = 150
# repeat_times = 50
# s = 'C:\\Users\\wangh\\Desktop\\组会\\聂子雄师兄\\第二篇论文\\unidelay\\data\\'
# distribution = 'Uniform'
# s = s + distribution + '-' + str(N) + '-100-1-100.txt'
# x = [0]
# y_multiMst = [0.0]
# y_MR = [0.0]
# y_GM = [0.0]
# n_step = 3
# for i in range(1, 9):
#     n = i * n_step
#     Q_multiMst = 0.0
#     Q_MR = 0.0
#     Q_GM = 0.0
#     for _ in range(repeat_times):
#         data_generation(N, 100)
#         nodes = pd.read_table(s, sep='\t', header=None)  # 读入txt文件，分隔符为\t
#         nodes.columns = ['label']
#         nodes['data.txt'] = None
#         nodes['posX'] = None
#         nodes['posY'] = None
#         for j in range(len(nodes)):  # 遍历每一行
#             coordinate = nodes['label'][j].split()  # 分开第i行，x列的数据。split()默认是以空格等符号来分割，返回一个列表
#             nodes['label'][j] = int(float(coordinate[0]))  # 分割形成的列表第一个数据给x列
#             nodes['data.txt'][j] = float(coordinate[1])  # 分割形成的列表第二个数据给y列
#             nodes['posX'][j] = float(coordinate[2])
#             nodes['posY'][j] = float(coordinate[3])
#         D = get_distance_matrix(nodes)
#         nodelist, coordinate, data = get_parameters(nodes)
#         path_multiMst, Q_multiMst_tp = multiMst(n, D, path_length, delay, data.txt)
#         path_MR, Q_MR_tp = MR_MinExpand(n, D, path_length, delay, data.txt)
#         path_GM, Q_GM_tp = G_MSCR(n, D, path_length, delay, data.txt)
#         Q_multiMst += Q_multiMst_tp / repeat_times
#         Q_MR += Q_MR_tp / repeat_times
#         Q_GM += Q_GM_tp / repeat_times
#     x.append(n)
#     y_MR.append(Q_MR)
#     y_multiMst.append(Q_multiMst)
#     y_GM.append(Q_GM)
# x = [0, 3, 6, 9, 12, 15, 18, 21, 24]
# y_multiMst = [0, 9885, 17003, 21964, 24986, 25218, 25156, 25212, 25068]
# y_MR = [0, 8899, 15399, 20125, 23747, 25293, 25213, 25276, 25149]
# y_GM = [0, 5179, 9908, 14195, 18230, 21586, 24096, 25262, 25149]
# print(x)
# print('y_multiMst:', y_multiMst)
# print('y_MR:', y_MR)
# print('y_GM:', y_GM)
# plt.xlim(0, 24.2)
# plt.ylim(0, 30000)  # 限定纵轴的范围
# plt.plot(x, y_multiMst, linewidth=1, marker='x', ms=5, label='MSTS')
# plt.plot(x, y_MR, linewidth=1, marker='o', ms=5, label='MR-MinExpand')
# plt.plot(x, y_GM, linewidth=1, marker='*', ms=5, label='G-MSCR')
# plt.legend()  # 让图例生效
# # plt.xticks(x, names, rotation=1)
# plt.margins(0)
# plt.subplots_adjust(bottom=0.10)
# plt.xlabel('Number of sensors m')  # X轴标签
# plt.ylabel("Total sensed data.txt(bytes)")  # Y轴标签
# # pyplot.yticks([0.750,0.800,0.850])
# plt.savefig('Sensors' + '-' + str(N) + '-' + str(path_length) + '-' + str(delay) + '.pdf', dpi=1000, format='pdf')
# plot_data = np.vstack((x, y_multiMst, y_MR, y_GM))
# np.savetxt('Sensors' + '-' + str(N) + '-' + str(path_length) + '-' + str(delay) + '.txt', plot_data, fmt='%d', delimiter=",")
