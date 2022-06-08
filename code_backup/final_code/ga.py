import random, math, sys
import matplotlib.pyplot as plt  # 画图
from copy import deepcopy
from tqdm import *  # 进度条
from data_preprocessing import *
from TSP_edges import *
from nx_draw import *
from nx_draw_old import *


DEBUG = False

geneNum = 100  # 种群数量
generationNum = 3000  # 迭代次数

CENTER = 0  # 配送中心

HUGE = 9999999
VARY = 0.1  # 变异几率


class Gene:
    def __init__(self, name='Gene', data=None):
        self.name = name
        self.length = n + m + 1
        if data is None:
            self.data = self._getGene(self.length)
        else:
            # assert(self.length+k == len(data))
            self.data = data
        self.fit = self.getFit()
        self.chooseProb = 0  # 选择概率

    # randomly choose a gene
    def _generate(self, length):
        data = [i for i in range(1, length)]
        random.shuffle(data)
        # print(data)
        data.insert(0, CENTER)
        data.append(CENTER)
        # print(data)
        return data

    # insert zeors at proper positions
    def _insertZeros(self, data):
        flag = k
        sum = 0
        newData = []
        for index, pos in enumerate(data):
            sum += t[pos]
            if sum > Q:
                newData.append(CENTER)
                flag = flag - 1
                sum = t[pos]
                if flag == 0:
                    return newData
            newData.append(pos)
        return newData

    # return a random gene with proper center assigned
    def _getGene(self, length):
        data = self._generate(length)
        data = self._insertZeros(data)
        return data

    # return fitness
    def getFit(self):
        fit = distCost = timeCost = overloadCost = fuelCost = 0
        dist = []  # from this to next

        # calculate distance
        i = 1
        while i < len(self.data):
            calculateDist = lambda x1, y1, x2, y2: math.sqrt(((x1 - x2) ** 2) + ((y1 - y2) ** 2))
            dist.append(calculateDist(X[self.data[i]], Y[self.data[i]], X[self.data[i - 1]], Y[self.data[i - 1]]))
            i += 1

        # distance cost
        distCost = sum(dist) * costPerKilo

        # time cost
        timeSpent = 0
        for i, pos in enumerate(self.data):
            # skip first center
            if i == 0:
                continue
            # new car
            elif pos == CENTER:
                timeSpent = 0
            # update time spent on road
            timeSpent += (dist[i - 1] / speed)
            # arrive early
            if timeSpent < eh[pos]:
                timeCost += ((eh[pos] - timeSpent) * epu)
                timeSpent = eh[pos]
            # arrive late
            elif timeSpent > lh[pos]:
                timeCost += ((timeSpent - lh[pos]) * lpu)
            # update time
            timeSpent += h[pos]

        # overload cost and out of fuel cost
        load = 0
        distAfterCharge = 0
        for i, pos in enumerate(self.data):
            # skip first center
            if i == 0:
                continue
            # charge here
            if pos > n:
                distAfterCharge = 0
            # at center, re-load
            elif pos == CENTER:
                load = 0
                distAfterCharge = 0
            # normal
            else:
                load += t[pos]
                distAfterCharge += dist[i - 1]
                # update load and out of fuel cost
                overloadCost += (HUGE * (load > Q))
                fuelCost += (HUGE * (distAfterCharge > dis))

        fit = distCost + timeCost + overloadCost + fuelCost
        return 1 / fit

    def updateChooseProb(self, sumFit):
        self.chooseProb = self.fit / sumFit

    def moveRandSubPathLeft(self):
        path = random.randrange(k)  # choose a path index
        index = self.data.index(CENTER, path + 1)  # move to the chosen index
        # move first CENTER
        locToInsert = 0
        self.data.insert(locToInsert, self.data.pop(index))
        index += 1
        locToInsert += 1
        # move data after CENTER
        while self.data[index] != CENTER:
            self.data.insert(locToInsert, self.data.pop(index))
            index += 1
            locToInsert += 1
        # assert(self.length+k == len(self.data))

    # plot this gene in a new window
    def plot(self):
        Xorder = [X[i] for i in self.data]
        Yorder = [Y[i] for i in self.data]
        plt.plot(Xorder, Yorder, c='black', zorder=1)
        plt.scatter(X, Y, zorder=2)
        plt.scatter([X[0]], [Y[0]], marker='o', zorder=5)
        plt.scatter(X[-m:], Y[-m:], marker='^', zorder=5)
        plt.title(self.name)
        plt.show()


def getSumFit(genes):
    sum = 0
    for gene in genes:
        sum += gene.fit
    return sum


# return a bunch of random genes
def getRandomGenes(size):
    genes = []
    for i in range(size):
        genes.append(Gene("Gene " + str(i)))
    return genes


# 计算适应度和
def getSumFit(genes):
    sumFit = 0
    for gene in genes:
        sumFit += gene.fit
    return sumFit


# 更新选择概率
def updateChooseProb(genes):
    sumFit = getSumFit(genes)
    for gene in genes:
        gene.updateChooseProb(sumFit)


# 计算累计概率
def getSumProb(genes):
    sum = 0
    for gene in genes:
        sum += gene.chooseProb
    return sum


# 选择复制，选择前 1/3
def choose(genes):
    num = int(geneNum / 6) * 2  # 选择偶数个，方便下一步交叉
    # sort genes with respect to chooseProb
    key = lambda gene: gene.chooseProb
    genes.sort(reverse=True, key=key)
    # return shuffled top 1/3
    return genes[0:num]


# 交叉一对
def crossPair(gene1, gene2, crossedGenes):
    gene1.moveRandSubPathLeft()
    gene2.moveRandSubPathLeft()
    newGene1 = []
    newGene2 = []
    # copy first paths
    centers = 0
    firstPos1 = 1
    for pos in gene1.data:
        firstPos1 += 1
        centers += (pos == CENTER)
        newGene1.append(pos)
        if centers >= 2:
            break
    centers = 0
    firstPos2 = 1
    for pos in gene2.data:
        firstPos2 += 1
        centers += (pos == CENTER)
        newGene2.append(pos)
        if centers >= 2:
            break
    # copy data not exits in father gene
    for pos in gene2.data:
        if pos not in newGene1:
            newGene1.append(pos)
    for pos in gene1.data:
        if pos not in newGene2:
            newGene2.append(pos)
    # add center at end
    newGene1.append(CENTER)
    newGene2.append(CENTER)
    # 计算适应度最高的
    key = lambda gene: gene.fit
    possible = []
    while gene1.data[firstPos1] != CENTER:
        newGene = newGene1.copy()
        newGene.insert(firstPos1, CENTER)
        newGene = Gene(data=newGene.copy())
        possible.append(newGene)
        firstPos1 += 1
    possible.sort(reverse=True, key=key)
    # assert(possible)
    crossedGenes.append(possible[0])
    key = lambda gene: gene.fit
    possible = []
    while gene2.data[firstPos2] != CENTER:
        newGene = newGene2.copy()
        newGene.insert(firstPos2, CENTER)
        newGene = Gene(data=newGene.copy())
        possible.append(newGene)
        firstPos2 += 1
    possible.sort(reverse=True, key=key)
    crossedGenes.append(possible[0])


# 交叉
def cross(genes):
    crossedGenes = []
    for i in range(0, len(genes), 2):
        crossPair(genes[i], genes[i + 1], crossedGenes)
    return crossedGenes


# 合并
def mergeGenes(genes, crossedGenes):
    # sort genes with respect to chooseProb
    key = lambda gene: gene.chooseProb
    genes.sort(reverse=True, key=key)
    pos = geneNum - 1
    for gene in crossedGenes:
        genes[pos] = gene
        pos -= 1
    return genes


# 变异一个
def varyOne(gene):
    varyNum = 10
    variedGenes = []
    for i in range(varyNum):
        p1, p2 = random.choices(list(range(1, len(gene.data) - 2)), k=2)
        newGene = gene.data.copy()
        newGene[p1], newGene[p2] = newGene[p2], newGene[p1]  # 交换
        variedGenes.append(Gene(data=newGene.copy()))
    key = lambda gene: gene.fit
    variedGenes.sort(reverse=True, key=key)
    return variedGenes[0]


# 变异
def vary(genes):
    for index, gene in enumerate(genes):
        # 精英主义，保留前三十
        if index < 30:
            continue
        if random.random() < VARY:
            genes[index] = varyOne(gene)
    return genes


if __name__ == "__main__":
    # todo 数据读取，不再写死

    S = 50  # 正方形边长
    n = 500  # 客户点数量
    m = 0  # 换电站数量
    k = 5  # 车辆数量
    Q = 100  # 额定载重量, kg
    dis = 750  # 续航里程, km
    costPerKilo = 30  # 油价
    epu = 0  # 早到惩罚成本
    lpu = 50  # 晚到惩罚成本
    speed = 90  # 速度，km/h

    ts_min = 60  # 最小的ts值，即最短的要求访问时间
    ts_max = 150  # 最大的ts值，即最长的要求访问时间
    nodes = get_nodes(n, S, ts_min, ts_max)
    nodelist, coordinate, lh_min, t = get_parameters(nodes)

    nodelist_copy = list(nodelist)

    lh = []
    for i in lh_min:
        lh.append(i / 60)

    lh[0] = 1000 / 60

    X = []
    Y = []

    for i in range(n + 1):
        X.append(coordinate[i][0])
        Y.append(coordinate[i][1])

    # 坐标 下列所有的第一个 都是基地的位置
    # X = [25,2.2468,17.0658,42.2267,20.2128,17.4451,24.2221,4.7710,2.2638,17.4722,7.5709,19.4573,22.3982,38.2522,24.0127,5.6469,27.3958,45.3375,17.6751,36.1443,27.6700,20.8482,17.5799,29.1898,12.2932,39.0355,48.2093,30.3208,9.8678,8.4249,15.4747,14.4859,5.5356,36.2468,44.6272,4.2779,30.2574,3.5905,33.9432,7.1292,25.4294,0.5989,49.6244,16.2737,28.6771,31.5127,25.0237,30.8373,8.8051,39.0680,39.3614]
    # Y = [25,11.8946,31.8810,49.4307,7.2127,5.2998,14.0996,33.9123,9.5269,21.2018,39.9020,24.8650,16.4311,42.8860,7.1213,17.1012,26.8355,27.7369,32.7309,32.7309,35.9695,4.0089,16.3734,28.4273,11.3295,45.0567,8.8480,49.9557,12.6903,25.5252,42.8352,42.1454,32.3151,36.4244,43.0788,10.1462,41.9299,1.8892,42.9472,27.3792,12.5857,28.1058,17.2975,28.5789,47.1603,35.9919,31.8560,34.4434,41.7107,19.0605,40.4705,22.6733]
    # X = [25, 2.2468, 17.0658, 42.2267, 20.2128, 17.4451, 24.2221, 4.7710, 2.2638, 17.4722, 7.5709, 19.4573, 22.3982, 38.2522, 24.0127, 5.6469, 27.3958, 45.3375, 17.6751, 36.1443, 27.6700, 20.8482, 17.5799, 29.1898, 12.2932,39.0355, 48.2093, 30.3208, 9.8678, 8.4249, 15.4747, 14.4859, 5.5356, 36.2468, 44.6272, 4.2779, 30.2574, 3.5905,33.9432, 7.1292, 25.4294, 0.5989, 49.6244, 16.2737, 28.6771, 31.5127, 25.0237, 30.8373, 8.8051, 39.0680,39.3614]
    # Y = [25, 11.8946, 31.8810, 49.4307, 7.2127, 5.2998, 14.0996, 33.9123, 9.5269, 21.2018, 39.9020, 24.8650, 16.4311,42.8860, 7.1213, 17.1012, 26.8355, 27.7369, 32.7309, 35.9695, 4.0089, 16.3734, 28.4273, 11.3295, 45.0567,8.8480, 49.9557, 12.6903, 25.5252, 42.8352, 42.1454, 32.3151, 36.4244, 43.0788, 10.1462, 41.9299, 1.8892,42.9472, 27.3792, 12.5857, 28.1058, 17.2975, 28.5789, 47.1603, 35.9919, 31.8560, 34.4434, 41.7107, 19.0605,40.4705, 22.6733]

    # 物资需求量
    # t = [0, 8, 10, 7, 8, 6, 10, 5, 8, 7, 15, 15, 6, 15, 15, 15, 7, 15, 15, 15, 6, 7, 10, 7, 15, 5, 15, 15, 7, 12, 7, 12,6, 12, 10, 10, 5, 10, 7, 8, 8, 6, 10, 5, 10, 6, 8, 7, 8, 5, 8]

    # 时间敏感性
    # lh = [1000 / 60, 126 / 60, 104 / 60, 92 / 60, 130 / 60, 131 / 60, 65 / 60, 118 / 60, 124 / 60, 97 / 60, 148 / 60,125 / 60, 69 / 60, 121 / 60, 128 / 60, 93 / 60, 88 / 60, 96 / 60, 110 / 60, 127 / 60, 136 / 60, 70 / 60,68 / 60, 126 / 60, 119 / 60, 99 / 60, 80 / 60, 72 / 60, 66 / 60, 75 / 60, 66 / 60, 98 / 60, 93 / 60, 80 / 60,138 / 60, 80 / 60, 149 / 60, 136 / 60, 120 / 60, 78 / 60, 138 / 60, 114 / 60, 127 / 60, 147 / 60, 103 / 60,61 / 60, 66 / 60, 61 / 60, 116 / 60, 82 / 60, 119 / 60]

    # 遗留问题
    # 服务时间
    h = []
    for i in range(n + 1):
        h.append(0)
    # 最早到达时间
    eh = []
    for i in range(n + 1):
        eh.append(0)

    genes = getRandomGenes(geneNum)  # 初始种群
    # 迭代
    for i in tqdm(range(generationNum)):
        updateChooseProb(genes)
        sumProb = getSumProb(genes)
        chosenGenes = choose(deepcopy(genes))  # 选择
        crossedGenes = cross(chosenGenes)  # 交叉
        genes = mergeGenes(genes, crossedGenes)  # 复制交叉至子代种群
        genes = vary(genes)  # under construction
    # sort genes with respect to chooseProb
    key = lambda gene: gene.fit
    genes.sort(reverse=True, key=key)  # 以fit对种群排序
    # 处理用到的无人机少于实际的无人机的情况
    freeuav = 0
    zerocount = 0
    for i in range(len(genes[0].data)):
        if genes[0].data[i] == 0:
            zerocount += 1
    freeuav = k + 1 - zerocount

    path = []

    zeroflag = 0
    insertflag = []

    for i in genes[0].data:
        if i == 0:
            zeroflag += 1

    for i in range(len(genes[0].data)):
        if genes[0].data[i] == 0:
            insertflag.append(i)

    pathcount = zeroflag - 1

    for i in range(pathcount):
        path.append([0])

    for i in range(len(insertflag) - 1):
        for j in range(insertflag[i], insertflag[i + 1]):
            path[i].append(genes[0].data[j + 1])

    edges = get_edges(path)

    print('\r\n')
    print('path:', path)
    print('data:', genes[0].data)
    print('fit:', genes[0].fit)
    print('free uav', freeuav)


    # genes[0].plot()  # 画出来
    nx_draw_old(nodelist_copy, coordinate, edges, 'ga.png')
