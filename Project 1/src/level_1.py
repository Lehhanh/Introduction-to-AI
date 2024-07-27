import numpy as np
from Node import *
from helper import*

directions = [(0, 1), (1, 0), (0, -1), (-1, 0)] #Right, Down, Left, Up

# Heuristic function: h(n) = sum of Manhattan distance of current position to goal position
def heuristic(currentPos, goalPos):
    return abs(currentPos[0] - goalPos[0]) + abs(currentPos[1] - goalPos[1])

# Breadth-first search
def BFS(map, startPos, goalPos):
    frontier = [Node(startPos, None, 0)]
    exploredSet = []
    while len(frontier) > 0:
        currentNode = frontier.pop(0)
        exploredSet.append(currentNode)
        neighborPos = currentNode.getNeighborPos(map)
        for neighbor in neighborPos:
            if neighbor == goalPos:
                return True, frontier, exploredSet
            if neighbor not in [n.position for n in frontier] and neighbor not in [n.position for n in exploredSet]:
                frontier.append(Node(neighbor, currentNode.position, currentNode.g_cost + 1))
    return False, frontier, exploredSet


# Uniform-cost search
def UCS(map, startPos, goalPos):
    frontier = [Node(startPos, None, 0)]
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
                    frontier.append(Node(neighbor, currentNode.position, currentNode.g_cost + 1))
                else:
                    index = [n.position for n in frontier].index(neighbor)
                    if currentNode.g_cost + 1 < frontier[index].g_cost:
                        frontier[index].updateCost(currentNode.g_cost + 1)
                        frontier[index].parent = currentNode.position
    return False, frontier, exploredSet


# Greedy best-first search
def GBFS(map, startPos, goalPos):
    frontier = [Node(startPos, None, 0, heuristic(startPos, goalPos))]
    exploredSet = []
    while len(frontier) > 0:
        frontier.sort(key=lambda n: n.h_cost)
        currentNode = frontier.pop(0)
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
def DFS(map, startPos, goalPos):
    frontier = [Node(startPos, None, 0)]
    exploredSet = []
    while len(frontier) > 0:
        currentNode = frontier.pop()
        if currentNode.position not in [n.position for n in exploredSet]:
            exploredSet.append(currentNode)
            if currentNode.position == goalPos:
                return True, frontier, exploredSet
            neighborPos = currentNode.getNeighborPos(map)
            for neighbor in neighborPos:
                frontier.append(Node(neighbor, currentNode.position, currentNode.g_cost + 1))
    return False, frontier, exploredSet



def pathFinding_level1(map):
    startPos = findPosition(map, 'S')[0]
    goalPos = findPosition(map, 'G')[0]
    pathList = []
    # BFS
    isSuccess, frontier, exploredSet = BFS(map, startPos, goalPos)
    if isSuccess:
        path = reconstructPath(exploredSet, startPos, goalPos, False)
    else:
        path = []
    pathList.append(path)
    # DFS
    isSuccess, frontier, exploredSet = DFS(map, startPos, goalPos)
    if isSuccess:
        path = reconstructPath(exploredSet, startPos, goalPos, True)
    else:
        path = []
    pathList.append(path)
    # UCS
    isSuccess, frontier, exploredSet = UCS(map, startPos, goalPos)
    if isSuccess:
        path = reconstructPath(exploredSet, startPos, goalPos, True)
    else:
        path = []
    pathList.append(path)
    # A*
    isSuccess, frontier, exploredSet = Astar(map, startPos, goalPos)
    if isSuccess:
        path = reconstructPath(exploredSet, startPos, goalPos, True)
    else:
        path = []
    pathList.append(path)
    # GBFS
    isSuccess, frontier, exploredSet = GBFS(map, startPos, goalPos)
    if isSuccess:
        path = reconstructPath(exploredSet, startPos, goalPos, False)
    else:
        path = []
    pathList.append(path)
    return pathList
