from operator import mul
from functools import reduce
from ortools.sat.python import cp_model
from itertools import product
from copy import copy

class MagicPrinter(cp_model.CpSolverSolutionCallback):
    def __init__(self, board):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.board = board
    
    def OnSolutionCallback(self):
        print(self.board)
        for cell in self.board.values():
            print(self.Value(cell))
            print()
        print()

class MagicModel(cp_model.CpModel):
    def __init__(self, board_dims, min_cell=1, **kwargs):
        self.board_dims = board_dims
        self.min_cell = min_cell
        super().__init__()
        self.setup()

    def setup(self):
        cell_cnt = reduce(mul, self.board_dims, 1)
        max_cell = self.min_cell + cell_cnt - 1
        twice_mean = self.min_cell + max_cell
        # if twice_mean is odd, and a board_dim is odd, it's not gonna work
        magic_sums = [twice_mean * board_dim // 2 for board_dim in self.board_dims]
        print(magic_sums)
        lines = {}
        self.board = {}
        # model = cp_model.CpModel()
        for cell in product(*[range(dim) for dim in self.board_dims]):
            new_int_var = self.NewIntVar(self.min_cell, max_cell, repr(cell))
            self.board[cell] = new_int_var
            for i in range(len(self.board_dims)):
                line_key = list(cell)
                line_key[i] = None
                line_key = tuple(line_key)
                line_val = lines.get(line_key)
                if not line_val:
                    line_val = []
                    lines[line_key] = line_val
                line_val.append(new_int_var)
        for line_item in lines.items():
            dim_num = line_item[0].index(None)
            self.Add(sum(line_item[1]) == magic_sums[dim_num])
        self.AddAllDifferent(self.board.values())
        self.solution_printer = MagicPrinter(self.board)

    def solve(self, **kwargs):
        show_solutions = kwargs.get('show_solutions')
        solver = cp_model.CpSolver()
        status = solver.SearchForAllSolutions(self, self.solution_printer)
        print(solver.StatusName(status))