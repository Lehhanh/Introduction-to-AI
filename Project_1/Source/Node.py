class Node:
    def __init__(self, position, parent, g_cost, h_cost=0, delivery_time=0, remain_fuel=0):
        self.position = position
        self.parent = parent
        self.g_cost = g_cost
        self.h_cost = h_cost
        self.f_cost = g_cost + h_cost
        self.delivery_time = delivery_time
        self.remain_fuel = remain_fuel


    def __lt__(self, other):
        return self.f_cost < other.f_cost
    
    def updateCost(self, g_cost, h_cost=0):
        self.g_cost = g_cost
        self.f_cost = g_cost + h_cost

    def getNeighborPos(self, map):
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)] #Right, Down, Left, Up
        neighbors = []
        for d in directions:
            newPos = tuple([a+b for a, b in zip(self.position, d)])
            if 0 <= newPos[0] < len(map) and 0 <= newPos[1] < len(map[0]) and map[newPos] != '-1':
                neighbors.append(newPos)
        return neighbors
