import numpy as np
from Node import *
from helper import *

directions = [(0, 1), (1, 0), (0, -1), (-1, 0)] #Right, Down, Left, Up

# Heuristic function: h(n) = sum of Manhattan distance of current position to goal position
def heuristic(currentPos, goalPos):
    return abs(currentPos[0] - goalPos[0]) + abs(currentPos[1] - goalPos[1])

# Breadth-first search
def BFS(map, startPos, goalPos):
    frontier = [Node(startPos, None, 0, 0)]
    exploredSet = []
    while len(frontier) > 0:
        currentNode = frontier.pop(0)
        exploredSet.append(currentNode)
        neighborPos = currentNode.getNeighborPos(map)
        for neighbor in neighborPos:
            if neighbor == goalPos:
                return True, frontier, exploredSet
            if neighbor not in [n.position for n in frontier] and neighbor not in [n.position for n in exploredSet]:
                frontier.append(Node(neighbor, currentNode.position, currentNode.g_cost + 1, 0))
    return False, frontier, exploredSet


# Uniform-cost search
def UCS(map, startPos, goalPos):
    frontier = [Node(startPos, None, 0, 0)]
    exploredSet = []
    while len(frontier) > 0:
        frontier.sort()
        currentNode = frontier.pop(0)
        exploredSet.append(currentNode)
        if currentNode.position == goalPos:
            return True, frontier, exploredSet
        neighborPos = currentNode.getNeighborPos(map)
        for neighbor in neighborPos:
            if neighbor not in [n.position for n in exploredSet]:
                if neighbor not in [n.position for n in frontier]:
                    frontier.append(Node(neighbor, currentNode.position, currentNode.g_cost + 1, 0))
                else:
                    index = [n.position for n in frontier].index(neighbor)
                    if currentNode.g_cost + 1 < frontier[index].g_cost:
                        frontier[index].updateCost(currentNode.g_cost + 1, 0)
                        frontier[index].parent = currentNode.position
    return False, frontier, exploredSet


# Greedy best-first search
def GBFS(map, startPos, goalPos):
    frontier = [Node(startPos, None, 0, heuristic(startPos, goalPos))]
    exploredSet = []
    while len(frontier) > 0:
        currentNode = frontier.pop([n.h_cost for n in frontier].index(min([n.h_cost for n in frontier])))
        exploredSet.append(currentNode)
        neighborPos = currentNode.getNeighborPos(map)
        for neighbor in neighborPos:
            if neighbor == goalPos:
                return True, frontier, exploredSet
            if neighbor not in [n.position for n in frontier] and neighbor not in [n.position for n in exploredSet]:
                frontier.append(Node(neighbor, currentNode.position, currentNode.g_cost + 1, heuristic(neighbor, goalPos)))
    return False, frontier, exploredSet


# A* search
def Astar(map, startPos, goalPos):
    frontier = [Node(startPos, None, 0, heuristic(startPos, goalPos))]
    exploredSet = []
    while len(frontier) > 0:
        frontier.sort()
        currentNode = frontier.pop(0)
        exploredSet.append(currentNode)
        if currentNode.position == goalPos:
            return True, frontier, exploredSet
        neighborPos = currentNode.getNeighborPos(map)
        for neighbor in neighborPos:
            if neighbor not in [n.position for n in exploredSet]:
                if neighbor not in [n.position for n in frontier]:
                    frontier.append(Node(neighbor, currentNode.position, currentNode.g_cost + 1, heuristic(neighbor, goalPos)))
                else:
                    index = [n.position for n in frontier].index(neighbor)
                    if currentNode.g_cost + 1 < frontier[index].g_cost:
                        frontier[index].updateCost(currentNode.g_cost + 1, frontier[index].h_cost)
                        frontier[index].parent = currentNode.position
    return False, frontier, exploredSet


# Depth-first search
def DFS(map, startPos, goalPos, path):
    frontier = [Node(startPos, None, 0, 0)]
    exploredSet = []
    while len(frontier) > 0:
        currentNode = frontier.pop()
        if currentNode.position not in [n.position for n in exploredSet]:
            exploredSet.append(currentNode)
            if currentNode.position == goalPos:
                return True
            for d in directions:
                newPos = tuple([a+b for a, b in zip(currentNode.position, d)])
                if 0 <= newPos[0] < len(map[0]) and 0 <= newPos[1] < len(map[1]) and newPos not in [n.position for n in exploredSet]:
                    frontier.append(Node(newPos, currentNode.position, 0, 0))


def pathfindingLevel_1(algorithm, map):
    startPos = [(index, row.index('S')) for index, row in enumerate(map) if 'S' in row][0]
    goalPos = [(index, row.index('G')) for index, row in enumerate(map) if 'G' in row][0]
    map = np.array(map)
    path = []
    if algorithm == 'BFS':
        isSuccess, frontier, exploredSet = BFS(map, startPos, goalPos)
        path = reconstructPath(exploredSet, startPos, goalPos, False)
    elif algorithm == 'UCS':
        isSuccess, frontier, exploredSet = UCS(map, startPos, goalPos)
        path = reconstructPath(exploredSet, startPos, goalPos, True)
    elif algorithm == 'GBFS':
        isSuccess, frontier, exploredSet = GBFS(map, startPos, goalPos)
        path = reconstructPath(exploredSet, startPos, goalPos, False)
    elif algorithm == 'Astar':
        isSuccess, frontier, exploredSet = Astar(map, startPos, goalPos)
        path = reconstructPath(exploredSet, startPos, goalPos, True)
    elif algorithm == 'DFS':
        isSuccess, frontier, exploredSet = DFS(map, startPos, goalPos)
    else:
        print('Algorithm is invaid')
        return -1
    if isSuccess:
        print('Frontier: ',[n.position for n in frontier])
        print('Explored Set: ', [n.position for n in exploredSet])
        print('Parent Set: ', [n.parent for n in exploredSet])
        print('Path:', path)
        print('Path cost: ', len(path) - 1)
    else:
        print('Cannat find any paths to destination') 
