
from G_MSCR import *
from data_generation import *
import numpy as np
import pandas as pd
from matplotlib import pyplot
import matplotlib.pyplot as plt
from whz import *
from WTSC import *
from MRMinExpand_new import *
from whz import *

#2的是最低20，相当于最低30但考虑起飞时间10分钟

if __name__ == '__main__':
    N = 100

    v = 25  # 无人机飞行速度，25m/s = 90km/h
    t_max = 10800  # 无人机续航时间，3h = 180min = 10800min
    omega = 5.7  # 无人机转弯角速度
    e = 0.2 #容忍系数


    x = [0]
    y_coverage_my = [0.0]
    y_onTime_my = [0.0]

    y_coverage_WTSC = [0.0]
    y_onTime_WTSC = [0.0]

    y_coverage_GMSCR = [0.0]
    y_onTime_GMSCR = [0.0]

    y_coverage_MR = [0.0]
    y_onTime_MR = [0.0]

    repeat_times = 50

    num_step = 1
    for i in range(1, 11): # 对于每一个x值区间
        num = i * num_step
        effective_coverage_rate_my = 0.0
        effective_coverage_rate_WTSC = 0.0
        effective_coverage_rate_GMSCR = 0.0
        effective_coverage_rate_MR = 0.0
        onTime_rate_my = 0.0
        onTime_rate_WTSC = 0.0
        onTime_rate_GMSCR = 0.0
        onTime_rate_MR = 0.0
        for _ in range(repeat_times): # 每一个x值对应的数据是跑repeat_times次出来的
            data_generation(N, 50,50,140)
            nodes = get_nodes(N,50,50,140)
            nodelist, coordinate, Data = get_parameters(nodes)
            nodelist_copy = list(nodelist)
            nodelist_copy2 = list(nodelist)
            D = get_distance_matrix(nodes)
            D *= 1000  # 千米换成米
            # 运行算法
            path_my, effective_coverage_rate_my_tmp, onTime_rate_my_tmp = my_method(num, nodelist, D, Data, v, omega, t_max,e)  # 此方法最后置空了nodelist
            path_WTSC,effective_coverage_rate_WTSC_tmp, onTime_rate_WTSC_tmp = WTSC(num, nodelist_copy, D, Data, v, omega, t_max,e)
            path_GMSCR,effective_coverage_rate_GMSCR_tmp,onTime_rate_GMSCR_tmp = G_MSCR(num, D, t_max, Data,v,omega,e)
            path_MR, effective_coverage_rate_MR_tmp, onTime_rate_MR_tmp = MRMinExpand(num,nodelist_copy2,D,Data,v,omega,t_max,e)

            # 结果取平均
            effective_coverage_rate_my += effective_coverage_rate_my_tmp/repeat_times
            onTime_rate_my += onTime_rate_my_tmp/repeat_times

            effective_coverage_rate_WTSC += effective_coverage_rate_WTSC_tmp/repeat_times
            onTime_rate_WTSC += onTime_rate_WTSC_tmp/repeat_times

            effective_coverage_rate_GMSCR += effective_coverage_rate_GMSCR_tmp/repeat_times
            onTime_rate_GMSCR += onTime_rate_GMSCR_tmp/repeat_times

            effective_coverage_rate_MR += effective_coverage_rate_MR_tmp / repeat_times
            onTime_rate_MR += onTime_rate_MR_tmp / repeat_times

        x.append(num)
        y_coverage_my.append(effective_coverage_rate_my)
        y_onTime_my.append(onTime_rate_my)
        y_coverage_WTSC.append(effective_coverage_rate_WTSC)
        y_onTime_WTSC.append(onTime_rate_WTSC)
        y_coverage_GMSCR.append(effective_coverage_rate_GMSCR)
        y_onTime_GMSCR.append(onTime_rate_GMSCR)
        y_coverage_MR.append(effective_coverage_rate_MR)
        y_onTime_MR.append(onTime_rate_MR)


    #
    # x = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    # y_coverage_my = [0.0, 0.42179999999999995, 0.7441999999999998, 0.9086, 0.9842, 0.9994000000000006,
    #                  1.0000000000000004, 1.0000000000000004, 1.0000000000000004, 1.0000000000000004, 1.0000000000000004]
    # y_coverage_WTSC = [0.0, 0.41540000000000005, 0.7182, 0.7823999999999997, 0.7719999999999998, 0.7966, 0.7802,
    #                    0.7711999999999998, 0.7689999999999998, 0.7809999999999998, 0.7772000000000001]
    # y_coverage_GMSCR = [0.0, 0.17780000000000007, 0.34919999999999995, 0.48200000000000004, 0.5965999999999997,
    #                     0.6724000000000001, 0.7275999999999999, 0.7394, 0.7320000000000001, 0.7403999999999997,
    #                     0.7256000000000001]
    # y_coverage_MR = [0.0, 0.3214000000000001, 0.5933999999999998, 0.7925999999999996, 0.9138, 0.9804,
    #                  0.9988000000000005, 1.0000000000000004, 1.0000000000000004, 1.0000000000000004, 1.0000000000000004]
    # y_onTime_my = [0.0, 0.3909999999999998, 0.6871999999999998, 0.8355999999999999, 0.9027999999999998,
    #                0.9155999999999999, 0.9191999999999998, 0.9170000000000001, 0.9177999999999996, 0.9193999999999999,
    #                0.9190000000000002]
    # y_onTime_WTSC = [0.0, 0.355, 0.6178000000000001, 0.6736, 0.667, 0.6811999999999998, 0.6658, 0.6591999999999998,
    #                  0.6524000000000001, 0.6748000000000001, 0.6726000000000001]
    # y_onTime_GMSCR = [0.0, 0.1514, 0.30500000000000005, 0.4099999999999999, 0.5114, 0.5750000000000002, 0.6192,
    #                   0.6259999999999997, 0.635, 0.638, 0.6234000000000002]
    # y_onTime_MR = [0.0, 0.2275999999999999, 0.4173999999999998, 0.5671999999999999, 0.6562000000000001,
    #                0.7187999999999999, 0.7237999999999997, 0.7114, 0.7374, 0.7282000000000003, 0.7225999999999999]

    print("x=",x)
    print("y_coverage_my=", y_coverage_my)
    print("y_coverage_WTSC=",y_coverage_WTSC)
    print("y_coverage_GMSCR=",y_coverage_GMSCR)
    print("y_coverage_MR=", y_coverage_MR)
    print("y_onTime_my=", y_onTime_my)
    print("y_onTime_WTSC=",y_onTime_WTSC)
    print("y_onTime_GMSCR=",y_onTime_GMSCR)
    print("y_onTime_MR=", y_onTime_MR)

    # plt.figure(figsize=(12, 4.5))
    # plt.subplot(121)
    # plt.xlim(0, 10)
    # plt.ylim(0, 1)  # 限定纵轴的范围
    # plt.plot(x, y_coverage_my, linewidth=1, marker='o', ms=5, color = '#FF7F0E',label='GCS')
    # plt.plot(x, y_coverage_WTSC, linewidth=1, marker='x', ms=5, color = '#1F77B4',label='WTSC')
    # plt.plot(x, y_coverage_GMSCR, linewidth=1, marker='*', ms=5, color='#2CA02C',label='G-MSCR')

    # 两率合在一起显示
    plt.plot(x, y_coverage_my, linewidth=1, marker='o', ms=5, color = '#FF4343',label='GCS-effective coverage rate')
    plt.plot(x, y_onTime_my, linewidth=1, marker='o', ms=5, color = '#FF4343',linestyle = '--',label='GCS-on time rate')
    plt.plot(x, y_coverage_WTSC, linewidth=1, marker='x', ms=5, color = '#1F77B4',label='WTSC-effective coverage rate')
    plt.plot(x, y_onTime_WTSC, linewidth=1, marker='x', ms=5, color = '#1F77B4',linestyle = '--',label='WTSC-on time rate')
    plt.plot(x, y_coverage_GMSCR, linewidth=1, marker='*', ms=5, color='#2CA02C',label='GMSCR-effective coverage rate')
    plt.plot(x, y_onTime_GMSCR, linewidth=1, marker='*', ms=5, color='#2CA02C',linestyle = '--',label='GMSCR-on time rate')
    plt.plot(x, y_coverage_MR, linewidth=1, marker='^', ms=5, color='#FF7F0E',label='MRMinExpand-effective coverage rate')
    plt.plot(x, y_onTime_MR, linewidth=1, marker='^', ms=5, color='#FF7F0E',linestyle = '--',label='MRMinExpand-on time rate')
    plt.legend()  # 让图例生效
    plt.margins(0)
    plt.subplots_adjust(bottom=0.10)
    plt.xlabel('Number of UAV')  # X轴标签
    plt.ylabel("effective coverage rate / on time rate")  # Y轴标签
    # plt.ylabel("effective coverage rate")  # Y轴标签

    # plt.subplot(122)
    # plt.xlim(0, 10)
    # plt.ylim(0, 1)  # 限定纵轴的范围
    # plt.plot(x, y_onTime_my, linewidth=1, marker='o', ms=5, color = '#FF7F0E',linestyle = '--',label='GCS')
    # plt.plot(x, y_onTime_WTSC, linewidth=1, marker='x', ms=5, color = '#1F77B4',linestyle = '--',label='WTSC')
    # plt.plot(x, y_onTime_GMSCR, linewidth=1, marker='*', ms=5, color='#2CA02C',linestyle = '--',label='G-MSCR')
    # plt.legend()  # 让图例生效
    # # plt.xticks(x, names, rotation=1)
    # plt.margins(0)
    # plt.subplots_adjust(bottom=0.10)
    # plt.xlabel('Number of UAV')  # X轴标签
    # plt.ylabel("on time rate")  # Y轴标签



    # pyplot.yticks([0.750,0.800,0.850])
    s = "./tcsPic/"
    plt.savefig(s+'CP-e1-UAV' + '-' + str(N)  + '.pdf', dpi=1000, format='pdf')
    plot_data = np.vstack((x,y_coverage_my, y_coverage_WTSC,y_coverage_GMSCR,y_coverage_MR,y_onTime_my, y_onTime_WTSC,y_onTime_GMSCR,y_onTime_MR))
    # plot_data = np.column_stack([x,y_coverage_my,y_coverage_WTSC])
    print("-----------")
    print(plot_data)
    np.savetxt(s+'CP-e1-UAV' + '-' + str(N) + '.txt', plot_data, fmt='%.3f', delimiter=",")

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
