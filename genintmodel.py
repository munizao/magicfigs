from operator import mul
from functools import reduce
from itertools import product
from more_itertools import all_equal
from copy import copy
from ortools.sat.python import cp_model
from ndlist import ndlist

class GenIntModel(cp_model.CpModel):
    def __init__(self, dims, min_cell=1, **kwargs):
        self.dims = dims
        self.min_cell = min_cell
        self.cell_cnt = reduce(mul, self.dims, 1)
        self.set_max_cell()

        super().__init__()

        twice_mean = self.min_cell + self.max_cell
        # if twice_mean is odd, and a board_dim is odd, it's not gonna work
        self.magic_sums = [twice_mean * dim // 2 for dim in self.dims]
        self.board = ndlist.empty(self.dims)
        self.board.total = twice_mean * self.cell_cnt // 2

        self.setup()
    
    def setup(self):
        for entry in product(*self.board.ranges):
            new_int_var = self.NewIntVar(self.min_cell, self.max_cell, repr(entry))
            self.board[entry] = new_int_var
    
    def remove_symmetries(self):
        # (Probably still broken when only some dims are equal.)
        origin = [0 for _ in self.dims]
        for i in range(1, 2 ** len(self.dims)):
            corner = [(self.dims[n] - 1) * ((i >> n) % 2) for n in range(len(self.dims))]
            self.Add(self.board[origin] <= self.board[corner])
        if all_equal(self.dims):
            for i, dim in enumerate(self.dims):
                corner = copy(origin)
                corner[i] = dim - 1
                if i == 0:
                    first_corner = corner
                    continue
                self.Add(self.board[first_corner] <= self.board[corner])
    
    def solve(self, **kwargs):
        # show_solutions = kwargs.get('show_solutions')
        solver = cp_model.CpSolver()
        status = solver.SearchForAllSolutions(self, self.solution_printer)
        print(solver.StatusName(status))