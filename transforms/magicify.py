from itertools import product
from copy import copy
from ndlist import ndlist

def magicify(board, min_cell=1):
    model = board.model
    subboard = ndlist(board.dims, 0)
    subboard.type = int
    model.boards.append(subboard)
    max_cell = min_cell + board.total - 1
    twice_mean = min_cell + max_cell
    subboard.magic_sums = [twice_mean * dim // 2 for dim in board.dims]

    ranges = [range(dim) for dim in subboard.dims]
    for entry in product(*ranges):
        new_int_var = model.NewIntVar(1, board.total, "^" + repr(entry))
        subboard[entry] = new_int_var
        line_ranges_by_dims = []
    for i in range(len(subboard.dims)):
        line_ranges = copy(ranges)
        line_ranges[i] = [None]
        line_ranges_by_dims.append(line_ranges)
    lines_by_dim = [[subboard[line] for line in product(*lrs)] 
        for lrs in line_ranges_by_dims]

    for dim_num, lines in enumerate(lines_by_dim):
        for line in lines:
            model.Add(sum(line) == subboard.magic_sums[dim_num])