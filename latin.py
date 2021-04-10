from itertools import product
from genintmodel import GenIntModel
from ndlist import ndlist
from solprinters import SolPrinter


class LatinModel(GenIntModel):
    def __init__(self, dims, min_cell=1, **kwargs):
        self.diagonals = kwargs.get('diagonals')
        self.max_cell = min_cell + max(dims) - 1
        super().__init__(dims, min_cell)
    
    def setup(self):
        for entry in product(*self.board.ranges):
            new_int_var = self.NewIntVar(self.min_cell, self.max_cell, repr(entry))
            self.board[entry] = new_int_var
        for lines in self.board.lines():
            for line in lines:
                self.AddAllDifferent(line)
        if self.diagonals:
            l = len(self.dims)
            sign_lists = [[1- ((n >> i) % 2) * 2 for i in range(l)] for n in range(2 ** (l - 1))]
            for signs in sign_lists:
                indices = [[i * sign - int(sign == -1)  for sign in signs] for i in range(self.dims[0])]
                self.AddAllDifferent([self.board[index] for index in indices])
        self.remove_symmetries()
        
        self.solution_printer = SolPrinter(self.board)
