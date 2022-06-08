##Data generation##
import numpy as np


def data_generation(N, S,ts_min,ts_max):
    #Ta = 10, 时间敏感性最低30，最高120
    q_min = ts_min
    q_max = ts_max
    lam = 50
    mu = 50



    index = [i for i in range(N + 1)] # 编号 0到N
    index = np.array(index)

    s = 'Uniform'
    data = np.random.randint(q_min, q_max + 1, size=N + 1) # 产生随机整数
    # data.txt = np.random.poisson(lam, size=N + 1)
    # data.txt = np.random.exponential(mu, size=N + 1)
    data[0] = 0

    D = np.random.uniform(0, S, size=(2, N + 1)) # 生成x,y坐标,第一行是横坐标，第二行是纵坐标

    D[0][0] = D[1][0] = 0 # 起点的x,y都设为0

    G = np.vstack((index, data, D)).T # np.vstack:按垂直方向（行顺序）堆叠数组构成一个新的数组,.T将矩阵转置

    # path = "C:\\Users\\lenovo\\sweep coverage\\data.txt sensing\\Delay\\unidelay\\data.txt\\"
    path = "C:\\Users\\hucon\\OneDrive\\文档\\毕业设计\\03.中期\\code\\whz"
    path = path + s + '-' + str(N) + '-' + str(S) + '-' + str(q_min) + '-' + str(q_max) + '.txt'
    # path = path + s + '-' + str(N) + '-' + str(S) + '-' + str(lam) + '.txt'
    # path = path + s + '-' + str(N) + '-' + str(S) + '-' + str(mu) + '.txt'
    np.savetxt(path, G, fmt='%.4f', delimiter='   ')



if __name__ == '__main__':
    # 1 base station, N POIs
    # N = 1000
    # size of square area is S by S
    S = 50
    # return time constraint
    # delay_min = 50
    # delay_max = 100
    for i in range(1, 21):
        N = i * 25
        data_generation(N, S,50,140)




