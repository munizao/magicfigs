from ndlist import ndlist
from itertools import product
from solprinters import SolPrinter

from ortools.sat.python import cp_model
class SparseModel(cp_model.CpModel):
    def __init__(self, dims, filled, syms=''):
        if type(dims) == int:
            dims = [dims for dim in range(2)]
        if type(filled) == int:
            filled = [filled for dim in dims]
        self.dims = dims
        self.filled = filled
        self.syms = syms
        self.board = ndlist.empty(dims)
        super().__init__()
        self.setup()
    
    def setup(self):
        for entry in product(*self.board.ranges):
            new_int_var = self.NewIntVar(0, 1, repr(entry))
            self.board[entry] = new_int_var
        for dim_num, lines in enumerate(self.board.lines()):
            for line in lines:
                self.Add(sum(line) == self.filled[dim_num])

        if 'h' in self.syms:
            for i in range(self.dims[0] // 2):
                for j in range(self.dims[1]):
                    self.Add(self.board[(i,j)] == self.board[(-i - 1, j)])
        
        if 's' in self.syms: 
            for i in range(self.dims[0] // 2):
                for j in range(self.dims[1]):
                    self.Add(self.board[(i,j)] == self.board[(-i - 1, -j - 1)])
        
        self.solution_printer = SolPrinter(self.board, type=bool)
    def solve(self, **kwargs):
        solver = cp_model.CpSolver()
        status = solver.SearchForAllSolutions(self, self.solution_printer)
        print(solver.StatusName(status))