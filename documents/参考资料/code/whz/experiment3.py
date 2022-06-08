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
    N = 100

    v = 25  # 无人机飞行速度，25m/s = 90km/h
    t_max = 10800  # 无人机续航时间，3h = 180min = 10800min
    omega = 5.7  # 无人机转弯角速度


    x = [0]
    y_coverage_my = [0.0]
    y_onTime_my = [0.0]

    y_coverage_WTSC = [0.0]
    y_onTime_WTSC = [0.0]

    y_coverage_GMSCR = [0.0]
    y_onTime_GMSCR = [0.0]

    repeat_times = 50

    num_step = 1
    for i in range(1, 11): # 对于每一个x值区间
        num = i * num_step
        effective_coverage_rate_my = 0.0
        effective_coverage_rate_WTSC = 0.0
        effective_coverage_rate_GMSCR = 0.0
        onTime_rate_my = 0.0
        onTime_rate_WTSC = 0.0
        onTime_rate_GMSCR = 0.0
        for _ in range(repeat_times): # 每一个x值对应的数据是跑repeat_times次出来的
            data_generation(N, 50)
            nodes = get_nodes(N,50)
            nodelist, coordinate, Data = get_parameters(nodes)
            nodelist_copy = list(nodelist)
            D = get_distance_matrix(nodes)
            D *= 1000  # 千米换成米
            # 运行算法
            path_my, effective_coverage_rate_my_tmp, onTime_rate_my_tmp = my_method(num, nodelist, D, Data, v, omega, t_max)  # 此方法最后置空了nodelist
            path_WTSC,effective_coverage_rate_WTSC_tmp, onTime_rate_WTSC_tmp = WTSC(num, nodelist_copy, D, Data, v, omega, t_max)
            path_GMSCR,effective_coverage_rate_GMSCR_tmp,onTime_rate_GMSCR_tmp = G_MSCR(num, D, t_max, Data,v,omega)

            # 结果取平均
            effective_coverage_rate_my += effective_coverage_rate_my_tmp/repeat_times
            onTime_rate_my += onTime_rate_my_tmp/repeat_times

            effective_coverage_rate_WTSC += effective_coverage_rate_WTSC_tmp/repeat_times
            onTime_rate_WTSC += onTime_rate_WTSC_tmp/repeat_times

            effective_coverage_rate_GMSCR += effective_coverage_rate_GMSCR_tmp/repeat_times
            onTime_rate_GMSCR += onTime_rate_GMSCR_tmp/repeat_times


        x.append(num)
        y_coverage_my.append(effective_coverage_rate_my)
        y_onTime_my.append(onTime_rate_my)
        y_coverage_WTSC.append(effective_coverage_rate_WTSC)
        y_onTime_WTSC.append(onTime_rate_WTSC)
        y_coverage_GMSCR.append(effective_coverage_rate_GMSCR)
        y_onTime_GMSCR.append(onTime_rate_GMSCR)

    # x = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    # y_coverage_my = [0.000, 0.424, 0.733, 0.902, 0.981, 0.999, 1.000, 1.000, 1.000, 1.000, 1.000]
    # y_onTime_my = [000, 0.393, 0.676, 0.828, 0.902, 0.920, 0.915, 0.921, 0.920, 0.919, 0.916]
    # y_coverage_WTSC = [0.000, 0.422, 0.689, 0.689, 0.692, 0.705, 0.695, 0.697, 0.699, 0.694, 0.694]
    # y_onTime_WTSC = [0.000, 0.357, 0.591, 0.589, 0.586, 0.598, 0.593, 0.596, 0.592, 0.589, 0.591]
    # y_coverage_GMSCR = [0.000, 0.184, 0.344, 0.492, 0.594, 0.686, 0.709, 0.735, 0.736, 0.732, 0.736]
    # y_onTime_GMSCR = [0.000, 0.158, 0.299, 0.416, 0.503, 0.587, 0.598, 0.633, 0.631, 0.626, 0.629]

    print("x=",x)
    print("y_coverage_my=",y_coverage_my)
    print("y_onTime_my=",y_onTime_my)
    print("y_coverage_WTSC=",y_coverage_WTSC)
    print("y_onTime_WTSC=",y_onTime_WTSC)
    print("y_coverage_GMSCR=",y_coverage_GMSCR)
    print("y_onTime_GMSCR=",y_onTime_GMSCR)


    # 设置图例并且设置图例的字体及大小
    font1 = {'family': 'Times New Roman',
             'weight': 'normal',
             'size': 12,
             }


    plt.xlim(0, 10)
    plt.ylim(0, 1)  # 限定纵轴的范围
    plt.plot(x, y_coverage_my, linewidth=1, marker='o', ms=5, color = '#FF7F0E',label='GCS')
    plt.plot(x, y_coverage_WTSC, linewidth=1, marker='x', ms=5, color = '#1F77B4',label='WTSC')
    plt.plot(x, y_coverage_GMSCR, linewidth=1, marker='*', ms=5, color='#2CA02C',label='G-MSCR')
    plt.legend(prop=font1)  # 让图例生效
    plt.margins(0)
    plt.subplots_adjust(bottom=0.10)
    plt.xlabel('Number of UAV', font1)  # X轴标签
    plt.ylabel("effective coverage rate", font1)  # Y轴标签
    plt.tick_params(labelsize=12)



    # pyplot.yticks([0.750,0.800,0.850])
    s = "./pic/"
    plt.savefig(s+'e3-70-160-UAV' + '-' + str(N)  + '.pdf', dpi=1000, format='pdf')
    plot_data = np.vstack((x, y_coverage_my,y_coverage_WTSC,y_coverage_GMSCR,y_onTime_my, y_onTime_WTSC,y_onTime_GMSCR))
    # plot_data = np.column_stack([x,y_coverage_my,y_coverage_WTSC])
    print("-----------")
    print(plot_data)
    np.savetxt(s+'e3-70-160-UAV' + '-' + str(N) + '.txt', plot_data, fmt='%.3f', delimiter=",")

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
