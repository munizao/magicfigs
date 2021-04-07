from itertools import product
from genmodel import GenModel
from ndlist import ndlist
from solprinters import SolPrinter


class LatinModel(GenModel):
    def __init__(self, dims, min_cell=1, **kwargs):
        self.max_cell = min_cell + max(dims) - 1
        super().__init__(dims, min_cell, *kwargs)
    
    def setup(self):
        for entry in product(*self.board.ranges):
            new_int_var = self.NewIntVar(self.min_cell, self.max_cell, repr(entry))
            self.board[entry] = new_int_var
        for lines in self.board.lines():
            for line in lines:
                self.AddAllDifferent(line)
        
        self.solution_printer = SolPrinter(self.board)
