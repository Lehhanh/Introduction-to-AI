import numpy as np
from Node import *
from helper import *
from level_2 import *

def searchAlgorithm_level3(map, start, goalPos, time_limit, fuel_limit):
    if time_limit <= 0:
        return False, []
    isSuccess, frontier, exploredSet = searchAlgorithm_level2(map, start, goalPos, time_limit)
    if isSuccess:
        path = reconstructPath(exploredSet, start, goalPos, True)
        if len(path) - 1 <= fuel_limit:
            return True, path
    # find all fuel station within fuel limit and time limit
    f_list, f_path = findFuelStation(map, start, goalPos, fuel_limit, time_limit)
    if len(f_list) == 0:
        return False, []
    for i in range(0, len(f_list)):
        isSuccess, path = searchAlgorithm_level3(map, f_list[i].position, goalPos, time_limit - f_list[i].delivery_time - getWaitTime(map, f_list[i].position), fuel_limit)
        if isSuccess:
            f_path[i] += path[1:]
    valid_path = [p for p in f_path if p[-1] == goalPos]
    if len(valid_path) > 0:
        d_time = [getDeliveryTime(map, p) for p in valid_path]
        min_time = min(d_time)
        index = d_time.index(min_time)
        return True, valid_path[index]
    return False, []

def findFuelStation(map, s, g, fuel_limit, time_limit):
    f = [Node(s, None, 0, heuristic(s, g), 0, fuel_limit)]
    e = []
    f_list = []
    while len(f) > 0:
        f.sort(key=lambda n: n.delivery_time + n.h_cost)
        currentNode = f.pop(0)
        e.append(currentNode)
        if 'F' in map[currentNode.position] and currentNode.position != s:
            f_list.append(currentNode)
        if currentNode.remain_fuel < 1:
            continue
        neighborPos = currentNode.getNeighborPos(map)
        for neighbor in neighborPos:
            if neighbor not in [n.position for n in e]:
                new_d_time = currentNode.delivery_time + 1
                if map[currentNode.position].isnumeric():
                    new_d_time += int(map[currentNode.position])
                if neighbor not in [n.position for n in f]:
                    if new_d_time + heuristic(neighbor, g) <= time_limit:
                        f.append(Node(neighbor, currentNode.position, currentNode.g_cost + 1, heuristic(neighbor, g), new_d_time, currentNode.remain_fuel - 1))
                else:
                    index = [n.position for n in f].index(neighbor)
                    if new_d_time < f[index].delivery_time:
                        f[index].delivery_time = new_d_time
                        f[index].updateCost(currentNode.g_cost + 1, f[index].h_cost)
                        f[index].parent = currentNode.position
    if len(f_list) > 0:
        f_list.sort(key=lambda n: n.h_cost + n.delivery_time)
        f_path = [reconstructPath(e, s, f_station.position, True) for f_station in f_list]
        return f_list, f_path
    return [], []


def pathFinding_level3(map, time_limit, fuel_limit):
    startPos = findPosition(map, 'S')[0]
    goalPos = findPosition(map, 'G')[0]
    isSuccess, path = searchAlgorithm_level3(map, startPos, goalPos, time_limit, fuel_limit)
    return path
