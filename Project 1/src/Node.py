import numpy as np
class Node:
    def __init__(self, position, parent, g_cost, h_cost):
        self.position = position
        self.parent = parent
        self.g_cost = g_cost
        self.h_cost = h_cost
        self.f_cost = g_cost + h_cost

    def __lt__(self, other):
        return self.f_cost < other.f_cost

    def getNeighborPos(self, map):
        map = np.array(map)
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)] #Right, Down, Left, Up
        neighbors = []
        for d in directions:
            newPos = tuple([a+b for a, b in zip(self.position, d)])
            if (0 <= newPos[0] < len(map) and 0 <= newPos[1] < len(map[0]) and map[newPos] != '-1'):
                neighbors.append(newPos)
        return neighbors
