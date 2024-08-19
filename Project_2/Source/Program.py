import numpy as np
class Program:
    def __init__(self, inputFilepath):
        self.read_world(inputFilepath)
        self.update_world()
    def read_world(self, inputFilepath):
        f = open(inputFilepath)
        self.size = int(f.readline())
        self.world = []
        for i in range (0, self.size):
            line = f.readline().strip().split('.')
            self.world.append(line)
        f.close()
    def get_size(self):
        return self.size
    def get_neighbors(self, position):
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        neighbors = []
        for d in directions:
            neighbor = [a+b for a, b in zip(position, d)]
            if 0 <= neighbor[0] < self.size and 0 <= neighbor[1] < self.size:
                neighbors.append(neighbor)
        return neighbors
    def get_components_cell(self, position):
        components = [] #include elements and percepts
        components_str = self.world[position[0]][position[1]]
        i = 0
        while i < len(components_str):
            if i+1 < len(components_str) and components_str[i+1] == '_':
                components.append(components_str[i:i+3])
                i += 3
            else:
                components.append(components_str[i])
                i += 1
        return components
    def update_world(self):
        for i in range (0, self.size):
            for j in range (0, self.size):
                if self.world[i][j] != '-':
                    components = self.get_components_cell([i, j])
                    if len(components) > 0:
                        percepts = ''
                        if 'W' in components:
                            percepts += 'S'
                        if 'P' in components:
                            percepts += 'B'
                        if 'P_G' in components:
                            percepts += 'W_H'
                        if 'H_P' in components:
                            percepts += 'G_L'
                        if len(percepts) > 0:
                            neighbors = self.get_neighbors([i, j])
                            for n in neighbors:
                                self.world[n[0]][n[1]] = self.world[n[0]][n[1]].replace('-', '')
                                self.world[n[0]][n[1]] += percepts
    def remove_components(self, position, component):
        self.world[position[0]][position[1]]= self.world[position[0]][position[1]].replace(component, '')
        if len(self.world[position[0]][position[1]]) == 0:
            self.world[position[0]][position[1]] = '-'
        if component == 'H_P':
            neighbors = self.get_neighbors(position)
            for n in neighbors:
                self.world[n[0]][n[1]] = self.world[n[0]][n[1]].replace('G_L', '') 
                if len(self.world[n[0]][n[1]]) == 0:
                    self.world[n[0]][n[1]] = '-'
        if component == 'W':
            neighbors = self.get_neighbors(position)
            for n in neighbors:
                self.world[n[0]][n[1]] = self.world[n[0]][n[1]].replace('S', '') 
                if len(self.world[n[0]][n[1]]) == 0:
                    self.world[n[0]][n[1]] = '-'

'''
Wumpus: W
Pit: P
Stench: S
Breeze: B
Gold: G
Whiff: W_H
Glow: G_L
Poisonous Gas: P_G
Healing Potions: H_P
'''