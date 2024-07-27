from Node import *
import numpy as np
#from UI import*

def readInput(filepath, level):
    map = []
    f = open(filepath)
    first_line = f.readline().split()
    row = int(first_line[0])
    col = int(first_line[1])
    for i in range(0, row):
        newRow = f.readline().split()
        map.append(newRow)
    map = np.array(map)
    if level > 1:
        t = int(first_line[2])
        if level == 2:
            return row, col, map, t
        if level == 3:
            f = int(first_line[3])
            return row, col, map, t, f
    return row, col, map

def createOutputFilepath(inputFilepath):
    i = inputFilepath.index('_')
    if i == -1:
        return ''
    outputFilepath = 'output' + inputFilepath[i - 1:]
    return outputFilepath

def writeOutput_level1(filepath, pathList):
    pass

def writeOutput(filepath, path):
    f = open(filepath, 'w')
    for i in range (0, len(path)):
        f.write(str(path[i]))
        if i < len(path) - 1:
            f.write(' ')
    f.close()

def findPosition(map, value):
    pos = [index for index, row in np.ndenumerate(map) if value in row]
    return pos

def reconstructPath(exploredSet, startPos, goalPos, isGinE):
    path = []
    if isGinE:
        i = [n.position for n in exploredSet].index(goalPos)
    else:
        i = len(exploredSet) - 1
        path.append(goalPos)
    while True:
        path = [exploredSet[i].position] + path
        if exploredSet[i].position == startPos:
            break
        i = [node.position for node in exploredSet].index(exploredSet[i].parent)
    return path

def getDeliveryTime(map, path):
    t = len(path) - 1
    for i in range (1, len(path) - 1):
        t += getWaitTime(map, path[i])
    return t

def getWaitTime(map, position):
    if map[position].isnumeric():
        return int(map[position])
    if 'F' in map[position]:
        temp = map[position][1:]
        if temp.isnumeric():
            return int(temp)
    return 0