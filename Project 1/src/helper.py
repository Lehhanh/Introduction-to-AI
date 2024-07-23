from Node import *

# Read input
def readInput(filepath):
    map = []
    f = open(filepath)
    row, col = f.readline().split()
    try:
        row = int(row)
        col = int(col)
        for i in range (0, row):
            line = f.readline()
            newRow = line.split()
            map.append(newRow)
    except:
        print('The number of row or column is invalid')
    return row, col, map

# Getting path from explored set
def reconstructPath(exploredSet, startPos, goalPos, isGinE):
    path = []
    i = len(exploredSet) - 1
    if not isGinE:
        path.append(goalPos)
    while True:
        path = [exploredSet[i].position] + path
        if exploredSet[i].position == startPos:
            break
        i = [node.position for node in exploredSet].index(exploredSet[i].parent)
    return path
