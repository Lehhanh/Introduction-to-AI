class Cell:
    def __init__(self, position, parent_cell, h_cost=0):
        self.position = position
        self.parent_cell = parent_cell
        self.h_cost = 0