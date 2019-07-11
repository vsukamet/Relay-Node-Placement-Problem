import math


def prims(N, G):
    node = 0
    MST = []
    edges = []
    visited = []

    while len(MST) != N - 1:
        min = float('inf')
        visited.append(node)
        for edge in G:
            if (edge[0] == node or edge[1] == node):
                edges.append(edge)

        if (len(visited) == N):
            break
        for edge in edges:
            if edge[2] < min and (edge[1] not in visited):
                min = edge[2]
                minEdge = edge

        edges.remove(minEdge)
        MST.append(minEdge)
        node = minEdge[1]
    return MST


def loadDataset(filename):
    with open(filename, "r") as filestream:
        c = 0
        for line in filestream:
            c = c + 1
    with open(filename, "r") as filestream:
        i = 0
        graph = []
        for line in filestream:
            dataset = line.split(" ")
            if (i == 0):
                N = int(dataset[0])
            if (i == 1):
                R = int(dataset[0])
            if (i == 2):
                B = int(dataset[0])
            if (i >= 3):
                graph.append([int(dataset[0]), int(dataset[1]), int(dataset[2])])
            i = i + 1
    return N, R, B, graph

print("Enter path of input file")
path= input()
N, R, B, graph = loadDataset(path)
MST = prims(N, graph)

for edge in MST:
    edge[2] = math.ceil(edge[2] / R) - 1


def sum_of_edges(MST):
    sum = 0
    for edge in MST:
        sum = sum + edge[2]
    return sum


sum = sum_of_edges(MST)
while (sum > B):
    max = 0
    for edge in MST:
        if (max < edge[2]):
            max = edge[2]
            max_edge = edge
    MST.remove(max_edge)
    sum = sum_of_edges(MST)
print("Resulting Forest for BCRP-MNCC is", MST)
