from ortools.sat.python import cp_model
from itertools import product
from ndlist import ndlist
from copy import copy

def metaify(model, cell_dims, **kwargs):
    board_dims = [model.dims[i] * cell_dims[i] for i in range(len(model.dims))]
    model.subboard = ndlist.empty(board_dims)
    ranges = [range(dim) for dim in board_dims]
    for entry in product(*ranges):
        new_int_var = model.NewIntVar(0, 1, "_" + repr(entry))
        model.subboard[entry] = new_int_var
    line_ranges_by_dims = []
    for i in range(len(board_dims)):
        line_ranges = copy(ranges)
        line_ranges[i] = [None]
        line_ranges_by_dims.append(line_ranges)
    # print([[line for line in product(*lrs)] for lrs in line_ranges_by_dims])
    lines_by_dim = [[model.subboard[line] for line in product(*lrs)] 
        for lrs in line_ranges_by_dims]
    for dim_num, lines in enumerate(lines_by_dim):
        for line in lines:
            model.Add(sum(line) == model.magic_sums[dim_num])

