def get_edges(path):
    edges = [] # edges由多个点对组成，两个点构成一条边
    edges = [[] for _ in range(len(path))]
    for sensor in range(len(path)):
        for i in range(len(path[sensor]) - 1):
            edges[sensor].append((path[sensor][i], path[sensor][i + 1]))
    return edges