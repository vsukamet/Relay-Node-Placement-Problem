import math
import sys


class Solution():

    def __init__(self, mst):
        self.mst = mst
        self.included = [False] * len(mst)
        self.upperBound = sys.maxsize


class VerticesSet():

    def __init__(self, v):
        self.v = v
        self.count = [0] * self.v

    def add(self, vertex):
        self.count[vertex] += 1

    def remove(self, vertex):
        if self.count[vertex] > 0:
            self.count[vertex] -= 1

    def numVertices(self):
        size = 0
        for i in range(self.v):
            if self.count[i] > 0:
                size += 1
        return size

    def isCircle(self, u, v):
        return self.count[u] > 0 and self.count[v] > 0


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


def calculateKMst(mst, k, i, count, currCost, verticesSet, sol, included):
    if count == k - 1 and verticesSet.numVertices() == k and currCost < sol.upperBound:
        sol.upperBound = currCost
        for j in range(len(included)):
            sol.included[j] = included[j]
        return

    if i >= len(mst) or count >= k - 1 or currCost > sol.upperBound:
        return

    u, v, weight = mst[i]
    isCircle = verticesSet.isCircle(u, v)
    shouldBacktrack = False
    if not isCircle:
        verticesSet.add(u)
        verticesSet.add(v)
        included[i] = True
        shouldBacktrack = True
        calculateKMst(mst, k, i + 1, count + 1, currCost + weight, verticesSet, sol, included)

    # Not include
    # backtrack
    # print("NOT including i: ", i)
    if shouldBacktrack:
        verticesSet.remove(u)
        verticesSet.remove(v)
        included[i] = False
    calculateKMst(mst, k, i + 1, count, currCost, verticesSet, sol, included)


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


if __name__ == "__main__":
    print("Enter Path of input file")
    path= input()
    numVertices, R, threshhold, graph = loadDataset(path)
    mst = prims(numVertices, graph)
    allSolutions = []
    for k1 in range(numVertices, 1, -1):
        verticesSet = VerticesSet(numVertices)
        sol = Solution(mst)
        included = [False] * len(mst)
        calculateKMst(mst, k=k1, i=0, count=0, currCost=0, verticesSet=verticesSet, sol=sol, included=included)
        numRelays = 0
        kmst = []
        for i in range(len(sol.included)):
            if sol.included[i]:
                numRelays += math.ceil(mst[i][2] / R) - 1
                kmst.append([mst[i][0], mst[i][1], math.ceil(mst[i][2] / R) - 1])

        if numRelays <= threshhold:
            print("Resulting Forest for BCRP-MLCC problem is ", kmst)
            connected_component = []
            for row in kmst:
                if (row[0] not in connected_component):
                    connected_component.append(row[0])
                if (row[1] not in connected_component):
                    connected_component.append(row[1])
            print("Size of Largest connected component is ", len(connected_component))
            break
