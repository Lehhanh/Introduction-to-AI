from Program import*

class Interface(Program):
    def __init__(self, inputFilepath, outputFilepath):
        Program.__init__(self, inputFilepath)
        self.fileOut = open(outputFilepath, 'w')
    def __del__(self):
        self.fileOut.close()
    def matrix_real_index(self, matrix_index):
        # col: first, row: second
        first = matrix_index[1] + 1
        second = self.get_world_size() - matrix_index[0]
        return [first, second]
    def real_matrix_index(self, real_index):
        # row: first, col: second
        first = self.get_world_size() - real_index[1]
        second = real_index[0] - 1
        return [first, second]
    def get_percept(self, real_index):
        matrix_index = self.real_matrix_index(real_index)
        components = self.get_components_cell(matrix_index)
        return components
    def get_world_size(self):
        return self.get_size()
    def grab_gold(self, cell):
        self.remove_components(self.real_matrix_index(cell), 'G')
    def grab_hp(self, cell):
        self.remove_components(self.real_matrix_index(cell), 'H_P')
    def shoot(self, cell):
        matrix_index = self.real_matrix_index(cell)
        components = self.get_components_cell(matrix_index)
        if 'W' in components:
            self.remove_components(matrix_index, 'W')
            return True #scream
        return False
    
i = Interface('test.txt', 'result1.txt')
print(i.get_percept((2, 3)))