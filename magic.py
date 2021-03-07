from operator import mul
from functools import reduce
from ortools.sat.python import cp_model
from itertools import product
from copy import copy

def model_magic(board_dims, min_cell=1, **kwargs):
    cell_cnt = reduce(mul, board_dims, 1)
    max_cell = min_cell + cell_cnt - 1
    total_sum = sum(range(min_cell, max_cell + 1))
    magic_sums = [total_sum // board_dim for board_dim in board_dims]
    lines = {}
    board = {}
    model = cp_model.CpModel()
    for cell in product(*[range(dim) for dim in board_dims]):
        new_int_var = model.NewIntVar(min_cell, max_cell, repr(cell))
        board[cell] = new_int_var
        for i in range(len(board_dims)):
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
        model.Add(sum(line_item[1]) == magic_sums[dim_num])
    model.AddAllDifferent(board.values())
    print(lines)
    return model, board

class SolutionPrinter(cp_model.CpSolverSolutionCallback):
    def __init__(self, board):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.board = board
    
    def OnSolutionCallback(self):
        print("got here")
        print(self.board)
        for cell in self.board.values():
            print(self.Value(cell))
            print()
        print()

def solve_magic(board_dims, min_cell=1, **kwargs):
    solver = cp_model.CpSolver()
    model, board = model_magic(board_dims, min_cell=1, **kwargs)
    if model:
        solution_printer = SolutionPrinter(board)
        print(solution_printer)
        status = solver.SearchForAllSolutions(model, solution_printer)
        print(status)