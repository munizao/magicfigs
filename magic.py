from operator import mul, eq
from functools import reduce
from ortools.sat.python import cp_model
from itertools import product
from more_itertools import collapse, all_equal
from copy import copy
from ndlist import ndlist
from solprinters import SolPrinter

class MagicModel(cp_model.CpModel):
    def __init__(self, dims, min_cell=1, **kwargs):
        self.diagonals = kwargs.get('diagonals')
        self.dims = dims
        self.min_cell = min_cell
        cell_cnt = reduce(mul, self.dims, 1)
        self.max_cell = self.min_cell + cell_cnt - 1
        twice_mean = self.min_cell + self.max_cell
        # if twice_mean is odd, and a board_dim is odd, it's not gonna work
        self.magic_sums = [twice_mean * board_dim // 2 for board_dim in self.dims]
        self.board = ndlist.empty(self.dims)
        self.board.total = twice_mean * cell_cnt // 2
        super().__init__()
        self.setup()

    def setup(self):
        for entry in product(*self.board.ranges):
            new_int_var = self.NewIntVar(self.min_cell, self.max_cell, repr(entry))
            self.board[entry] = new_int_var
        for dim_num, lines in enumerate(self.board.lines()):
            for line in lines:
                self.Add(sum(line) == self.magic_sums[dim_num])
        if self.diagonals:
            l = len(self.dims)
            sign_lists = [[1- ((n >> i) % 2) * 2 for i in range(l)] for n in range(2 ** (l - 1))]
            for signs in sign_lists:
                indices = [[i * sign - int(sign == -1)  for sign in signs] for i in range(self.dims[0])]
                self.Add(sum([self.board[index] for index in indices]) == self.magic_sums[0])
        self.AddAllDifferent(collapse(self.board))
        # Remove redundant symmetries.  (Probably still broken when only some dims are equal.)
        origin = [0 for _ in self.dims]
        for i in range(1, 2 ** len(self.dims)):
            corner = [(self.dims[n] - 1) * ((i >> n) % 2) for n in range(len(self.dims))]
            self.Add(self.board[origin] < self.board[corner])
        if all_equal(self.dims):
            for i, dim in enumerate(self.dims):
                corner = copy(origin)
                corner[i] = dim - 1
                if i == 0:
                    first_corner = corner
                    continue
                self.Add(self.board[first_corner] < self.board[corner])

        self.solution_printer = SolPrinter(self.board)

    def solve(self, **kwargs):
        show_solutions = kwargs.get('show_solutions')
        solver = cp_model.CpSolver()
        status = solver.SearchForAllSolutions(self, self.solution_printer)
        print(solver.StatusName(status))
