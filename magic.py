from operator import mul
from functools import reduce
from ortools.sat.python import cp_model
from itertools import product
from more_itertools import collapse
from copy import copy
from ndlist import ndlist
from solprinters import SolPrinter

class MagicModel(cp_model.CpModel):
    def __init__(self, dims, min_cell=1, **kwargs):
        self.dims = dims
        self.min_cell = min_cell
        cell_cnt = reduce(mul, self.dims, 1)
        self.max_cell = self.min_cell + cell_cnt - 1
        super().__init__()
        self.setup()

    def setup(self):
        twice_mean = self.min_cell + self.max_cell
        # if twice_mean is odd, and a board_dim is odd, it's not gonna work
        self.magic_sums = [twice_mean * board_dim // 2 for board_dim in self.dims]
        print("magic sums", self.magic_sums)
        lines = {}
        self.board = ndlist.empty(self.dims)
        for entry in product(*self.board.ranges):
            new_int_var = self.NewIntVar(self.min_cell, self.max_cell, repr(entry))
            self.board[entry] = new_int_var
        for dim_num, lines in enumerate(self.board.lines()):
            for line in lines:
                self.Add(sum(line) == self.magic_sums[dim_num])
        self.AddAllDifferent(collapse(self.board))
        # Remove redundant symmetries.  So far, this only catches reflections
        origin = [0 for _ in self.dims]
        for i in range(2 ** len(self.dims)):
            corner = [(self.dims[n] - 1) * ((i >> n) % 2) for n in range(len(self.dims))]
            self.Add(self.board[origin] <= self.board[corner])
        self.solution_printer = SolPrinter(self.board)

    def solve(self, **kwargs):
        show_solutions = kwargs.get('show_solutions')
        solver = cp_model.CpSolver()
        status = solver.SearchForAllSolutions(self, self.solution_printer)
        print(solver.StatusName(status))
