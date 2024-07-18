import numpy as np

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
    return map


directions = [(0, 1), (1, 0), (0, -1), (-1, 0)] #Right, Down, Left, Up
def BFS(map, start, goal):
    frontier = [start]
    exploredSet = []
    while (len(frontier) > 0):
        currentPos = frontier.pop(0)
        exploredSet.append(currentPos)

        print(currentPos)
        for d in directions:
            newPos = tuple([a+b for a, b in zip(currentPos, d)])
            print('newPos', newPos)
            if newPos == goal:
                print('Goal')
                return 1, frontier, exploredSet
            if 0 <= newPos[0] < len(map[0]) and 0 <= newPos[1] < len(map) and map[newPos] != '-1' and newPos not in exploredSet and newPos not in frontier:
                print('append frontier')
                frontier.append(newPos)
    return -1, frontier, exploredSet


# Test với input ngắn cho dễ kiểm tra với kết quả chạy tay
m = readInput('text.txt')
if len(m) > 0:
    m = np.array(m)
    print(m)
    isSuccess, frontier, exploredSet = BFS(m, (0, 0), (4, 4))
    print(frontier)
    print(exploredSet)
# m = readInput('input1_level1.txt')