from sympy import *
from Interface import *
from Cell import *
# direction: (dx, dy)
direction_priority = {
    'N': [(0, 1), (1, 0), (-1, 0), (0, -1)],
    'E': [(1, 0), (0, 1), (0, -1), (-1, 0)],
    'S': [(0, -1), (1, 0), (-1, 0), (0, 1)],
    'W': [(-1, 0), (0, 1), (0, -1), (1, 0)]
}

turn_action = {
    ('N', 'E'): ['TURN_RIGHT'],
    ('N', 'W'): ['TURN_LEFT'],
    ('N', 'S'): ['TURN_RIGHT', 'TURN_RIGHT'],
    ('S', 'E'): ['TURN_LEFT'],
    ('S', 'W'): ['TURN_RIGHT'],
    ('S', 'N'): ['TURN_RIGHT', 'TURN_RIGHT'],
    ('E', 'N'): ['TURN_LEFT'],
    ('E', 'S'): ['TURN_RIGHT'],
    ('E', 'W'): ['TURN_RIGHT', 'TURN_RIGHT'],
    ('W', 'N'): ['TURN_RIGHT'],
    ('W', 'S'): ['TURN_LEFT'],
    ('W', 'E'): ['TURN_RIGHT', 'TURN_RIGHT'],
}

direction_turn = {
    ('N', 'TURN_RIGHT'): 'E',
    ('N', 'TURN_LEFT'): 'W',
    ('S', 'TURN_RIGHT'): 'W',
    ('S', 'TURN_LEFT'): 'E',
    ('E', 'TURN_RIGHT'): 'S',
    ('E', 'TURN_LEFT'): 'N',
    ('W', 'TURN_RIGHT'): 'N',
    ('W', 'TURN_LEFT'): 'S'
}

def heuristic(src, des):
    return abs(src[0] - des[0]) + abs(src[0] - des[0])

class Agent:
    def __init__(self, interface):
        self.point = 0
        self.health = 100
        self.hp = 0
        self.visited_cell = []
        self.current_cell = (1, 1)
        self.parent_cell = None
        self.direction = 'N'
        self.KB = set()
        self.is_alive = True
        self.interface = interface
        self.world_size = interface.get_world_size()
    def infer(self, conclusion):
        # KB => a iff KB & ~a is unsatisfiable
        return not satisfiable(And(*self.KB, Not(conclusion)))
    def get_neighbors_agent(self, current_cell):
        neighbors = []
        for d in direction_priority[self.direction]:
            neighbor = tuple([a+b for a, b in zip(current_cell, d)])
            if 0 < neighbor[0] <= self.world_size and 0 < neighbor[1] <= self.world_size:
                neighbors.append(neighbor)
        return neighbors
    def update_agent(self):
        neighbor = list(set(self.get_neighbors_agent(self.current_cell)).difference(self.visited_cell))
        percept = self.interface.get_percept(self.current_cell)
        if 'W' in percept:
            self.point -= 10000
            self.is_alive = False
        else: 
            self.KB.add(Not(symbols(f'W{self.current_cell[0]}{self.current_cell[1]}')))
        if 'P' in percept:
            self.point -= 10000
            self.is_alive = False
        else:
            self.KB.add(Not(symbols(f'P{self.current_cell[0]}{self.current_cell[1]}')))
        if 'G' in percept:
            self.point -= 10
            self.point += 5000
            self.interface.grab_gold(self.current_cell)
            self.interface.fileOut.write(f'{str(self.current_cell)}: GRAB_GOLD: {str(self.direction)}: {str(self.health)}: {str(self.point)}: {self.hp}\n')
        if 'P_G' in percept:
            self.health -= 25
            if self.health <= 0:
                self.is_alive = False
                return
            if self.health == 25 and self.hp > 0:
                self.hp -= 1
                self.point -= 10
                self.health += 25
                self.interface.fileOut.write(f'{str(self.current_cell)}: HEAL: {str(self.direction)}: {str(self.health)}: {str(self.point)}: {self.hp}\n')
        if 'H_P' in percept:
            self.point -= 10
            self.hp += 1
            self.interface.grab_hp(self.current_cell)
            self.interface.fileOut.write(f'{str(self.current_cell)}: GRAB_HP: {str(self.direction)}: {str(self.health)}: {str(self.point)}: {self.hp}\n')
            if self.health <= 25:
                self.hp -= 1
                self.point -= 10
                self.health += 25
                self.interface.fileOut.write(f'{str(self.current_cell)}: HEAL: {str(self.direction)}: {str(self.health)}: {str(self.point)}: {self.hp}\n')
        if 'S' in percept:
            self.KB.add(symbols(f'S{self.current_cell[0]}{self.current_cell[1]}'))
            temp = set()
            for n in neighbor:
                temp.add(symbols(f'W{n[0]}{n[1]}'))
                neighbor1 = list(set(self.get_neighbors_agent(n)).difference(self.visited_cell))
                temp1 = set()
                for n1 in neighbor1:
                    temp1.add(symbols(f'S{n1[0]}{n1[1]}'))
                self.KB.add(Equivalent(symbols(f'W{n[0]}{n[1]}'), And(*temp1)))
            self.KB.add(Equivalent(symbols(f'S{self.current_cell[0]}{self.current_cell[1]}'), Or(*temp)))
        else:
            self.KB.add(Not(symbols(f'S{self.current_cell[0]}{self.current_cell[1]}')))
            for n in neighbor:
                self.KB.add(Not(symbols(f'W{n[0]}{n[1]}')))
        if 'B' in percept:
            self.KB.add(symbols(f'B{self.current_cell[0]}{self.current_cell[1]}'))
            temp = set()
            for n in neighbor:
                temp.add(symbols(f'P{n[0]}{n[1]}'))
                neighbor1 = list(set(self.get_neighbors_agent(n)).difference(self.visited_cell))
                temp1 = set()
                for n1 in neighbor1:
                    temp1.add(symbols(f'B{n1[0]}{n1[1]}'))
                self.KB.add(Equivalent(symbols(f'P{n[0]}{n[1]}'), And(*temp1)))
            self.KB.add(Equivalent(symbols(f'B{self.current_cell[0]}{self.current_cell[1]}'), Or(*temp)))
        else:
            self.KB.add(Not(symbols(f'B{self.current_cell[0]}{self.current_cell[1]}')))
            for n in neighbor:
                self.KB.add(Not(symbols(f'P{n[0]}{n[1]}')))
        if 'W_H' in percept:
            self.KB.add(symbols(f'W_H{self.current_cell[0]}{self.current_cell[1]}'))
            temp = set()
            for n in neighbor:
                temp.add(symbols(f'P_G{n[0]}{n[1]}'))
                neighbor1 = list(set(self.get_neighbors_agent(n)).difference(self.visited_cell))
                temp1 = set()
                for n1 in neighbor1:
                    temp1.add(symbols(f'W_H{n1[0]}{n1[1]}'))
                self.KB.add(Equivalent(symbols(f'P_G{n[0]}{n[1]}'), And(*temp1)))
            self.KB.add(Or(*temp))
        else:
            self.KB.add(Not(symbols(f'W_H{self.current_cell[0]}{self.current_cell[1]}')))
            for n in neighbor:
                self.KB.add(Not(symbols(f'P_G{n[0]}{n[1]}')))
    def check_wumpus(self, cell):
        # check W
        if self.infer(symbols(f'W{cell[0]}{cell[1]}')):
            return True
        # check ~W
        if self.infer(Not(symbols(f'W{cell[0]}{cell[1]}'))):
            return False
        return None
    def check_pit(self, cell):
        # check P
        if self.infer(symbols(f'P{cell[0]}{cell[1]}')):
            return True
        # check ~P
        if self.infer(Not(symbols(f'P{cell[0]}{cell[1]}'))):
            return False
        return None
    def find_shortest_path(self, src_cell, des_cell):
        # find path base on GBFS
        # rescontruct path from explored set
        def reconstructPath(explored, src_cell, des_cell):
            path = []
            i = len(explored) - 1
            path.append(des_cell)
            while True:
                path = [explored[i].position] + path
                if explored[i].position == src_cell:
                    break
                i = [node.position for node in explored].index(explored[i].parent_cell)
            return path
        frontier = [Cell(src_cell, None, heuristic(src_cell, des_cell))]
        explored = []
        while len(frontier) > 0:
            frontier.sort(key=lambda c: c.h_cost)
            cell = frontier.pop(0)
            explored.append(cell)
            neighbors = list(set(self.get_neighbors_agent(cell.position)).intersection(self.visited_cell))
            for neighbor in neighbors:
                if neighbor == des_cell:
                    return True, reconstructPath(explored, src_cell, des_cell)
                if neighbor not in [c.position for c in frontier] and neighbor not in [c.position for c in explored]:
                    frontier.append(Cell(neighbor, cell.position, heuristic(neighbor, des_cell)))
        return False, []
    def turn(self, cell):
        temp = tuple([a-b for a, b in zip(cell, self.current_cell)])
        '''
        direction:
        N = (0, 1)
        S = (0, -1)
        E = (1, 0)
        W = (-1, 0)
        '''
        d = ''
        if temp == (0, 1):
            d = 'N'
        if temp == (0, -1):
            d = 'S'
        if temp == (1, 0):
            d = 'E'
        if temp == (-1, 0):
            d = 'W'
        if self.direction != d:
            action = turn_action[(self.direction, d)]
            current_direction = self.direction
            for a in action:
                self.point -= 10
                current_direction = direction_turn[(current_direction, a)]
                self.interface.fileOut.write(f'{str(self.current_cell)}: {a}: {str(current_direction)}: {str(self.health)}: {str(self.point)}: {self.hp}\n')
            self.direction = d
    def shoot_wumpus(self, cell):
        # turn agent face to wumpus
        self.turn(cell)
        self.point -= 100
        self.interface.fileOut.write(f'{str(self.current_cell)}: SHOOT: {str(self.direction)}: {str(self.health)}: {str(self.point)}: {self.hp}\n')
        # shoot agent and update map
        scream = self.interface.shoot(cell)
        # Update KB for agent
        self.KB.add(Not(symbols(f'W{cell[0]}{cell[1]}')))
        neighbors = self.get_neighbors_agent(cell)
        for n in neighbors:
            self.KB.add(Not(symbols(f'S{cell[0]}{cell[1]}')))
        return scream
    def move_adj_cell(self, next_cell):
        # turn agent face to next cell
        self.turn(next_cell)
        self.point -= 10
        self.interface.fileOut.write(f'{str(self.current_cell)}: MOVE_FORWARD: {str(self.direction)}: {str(self.health)}: {str(self.point)}: {self.hp}\n')
        # update agent's info
        self.parent_cell = self.current_cell
        self.current_cell = next_cell
    def move_back(self, des_cell):
        # find the shortest path that only has visited cells
        isSucess, path = self.find_shortest_path(self.current_cell, des_cell)
        # move sequentially
        self.move_adj_cell(path[1])
        for i in range (2, len(path)):
            self.update_agent()
            if self.is_alive == False:
                return False
            self.move_adj_cell(path[i])
        return True
    def is_adj_cell(self, cell1, cell2):
        # the difference between two position (element-wise)
        temp = tuple([a-b for a, b in zip(cell1, cell2)])
        if temp == (1, 0) or temp == (0, 1) or temp == (-1, 0) or temp == (0, -1):
            return True
        return False
    def explore_world(self):
        # stack of safe cells
        stack = []

        # explore the map untill agent die or no more safe cells
        while self.is_alive:
            # agent get percepts and add KB in this cell
            self.update_agent()
            # check if agent died
            if self.is_alive == False:
                print('Agent is dead')
                break
            # mark as visited cell
            self.visited_cell.append(self.current_cell)
            # get neighbor cell that is not in visited list
            temp = self.get_neighbors_agent(self.current_cell)
            neighbors = []
            for n in temp:
                if n not in self.visited_cell:
                    neighbors.append(n)
            # check safe cells
            safe_neighbors = []
            for n in neighbors:
                percepts = self.interface.get_percept(self.current_cell)
                wumpus = False
                pit = False
                if 'S' in percepts:
                    wumpus = self.check_wumpus(n)
                    if wumpus == True:
                        scream = self.shoot_wumpus(n)
                        wumpus = False
                if 'B' in percepts:
                    pit = self.check_pit(n)
                if wumpus == False and pit == False:
                    safe_neighbors.append(n)
            # add all safe cells to stack
            safe_neighbors.reverse()
            for n in safe_neighbors:
                if n in stack:
                    stack.remove(n)
            stack += safe_neighbors
            # check if no more safe cell
            if len(stack) == 0:
                break
            next_cell = stack.pop()
            # do not need to explore the cell in visited list
            while next_cell in self.visited_cell:
                next_cell = stack.pop()
            temp = (1, 1)
            # find the nearest safe cell
            if not self.is_adj_cell(self.current_cell, next_cell):
                for i in range(len(self.visited_cell) - 1, -1 , -1):
                    if self.is_adj_cell(next_cell, self.visited_cell[i]):
                        temp = self.visited_cell[i]
                # move to the adjacent cell (visited) of this safe cell
                self.move_back(temp)
            # move to next cell
            self.move_adj_cell(next_cell)
        if self.is_alive == True:
            # move to the start positon
            isSuccess = self.move_back((1, 1))
            if isSuccess:
                self.point += 10
                self.interface.fileOut.write(f'{str(self.current_cell)}: CLIMB: {str(self.direction)}: {str(self.health)}: {str(self.point)}: {self.hp}\n')
        # the agent is dead
        if self.is_alive == False:
            self.interface.fileOut.write(f'{str(self.current_cell)}: DIE: {str(self.direction)}: {str(self.health)}: {str(self.point)}: {self.hp}\n')
            print('Agent is dead')
        self.interface.fileOut.close()

i = Interface('map1.txt', 'result1.txt')
a = Agent(i) 