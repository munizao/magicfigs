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
    model = cp_model.CpModel()
    for cell in product(*[range(dim) for dim in board_dims]):
        new_int_var = model.NewIntVar(0, 1, repr(cell))
        for i in len(board_dims):
            line_key = copy(cell)
            line_key[i] = None
            line_key = tuple(line_key)
            line_val = lines.get(line_key)
            if not line_val:
                line_val = []
                lines.line_key = line_val
            line_val.append(new_int_var)
    for line_item in lines.items:
        model.Add(sum(line_item[0]) == magic_sums[n])

