import numpy as np
from Node import *
from helper import *
from level_1 import *

def searchAlgorithm_level2(map, startPos, goalPos, time_limit):
    frontier = [Node(startPos, None, 0, heuristic(startPos, goalPos))]
    exploredSet = []
    while len(frontier) > 0:
        frontier.sort(key=lambda n: n.delivery_time + n.h_cost)
        currentNode = frontier.pop(0)
        exploredSet.append(currentNode)
        if currentNode.delivery_time > time_limit:
            break
        if currentNode.position == goalPos:
            return True, frontier, exploredSet
        neighborPos = currentNode.getNeighborPos(map)
        for neighbor in neighborPos:
            if neighbor not in [n.position for n in exploredSet]:
                new_delivery_time = currentNode.delivery_time + 1
                if map[currentNode.position].isnumeric():
                    new_delivery_time += int(map[currentNode.position])
                if neighbor not in [n.position for n in frontier]:
                    frontier.append(Node(neighbor, currentNode.position, currentNode.g_cost + 1, heuristic(neighbor, goalPos), new_delivery_time))
                else:
                    index = [n.position for n in frontier].index(neighbor)
                    if new_delivery_time < frontier[index].delivery_time:
                        frontier[index].delivery_time = new_delivery_time
                        frontier[index].parent = currentNode.position
    return False, frontier, exploredSet


def pathFinding_level2(map, time_limit):
    startPos = findPosition(map, 'S')[0]
    goalPos = findPosition(map, 'G')[0]
    path = []
    isSuccess, frontier, exploredSet = searchAlgorithm_level2(map, startPos, goalPos, time_limit)
    if isSuccess:
        path = reconstructPath(exploredSet, startPos, goalPos, True)
    return path