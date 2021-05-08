from ortools.sat.python import cp_model
from itertools import product
from more_itertools import all_equal
from functools import reduce
from operator import mul
from copy import copy
from ndlist import ndlist

def metaify(board, cell_dims, **kwargs):
    model = board.model
    diagonals = kwargs.get('diagonals')
    kitty_corners = kwargs.get('kitty_corners')
    puddleless = kwargs.get('puddleless')
    crinkles = kwargs.get('crinkles')
    translate_swap = kwargs.get('translate_swap')
    cell_size = reduce(mul, cell_dims, 1)
    subboard_dims = [board.dims[i] * cell_dims[i] for i in range(len(board.dims))]
    subboard = ndlist(subboard_dims)

    subboard.type = bool
    subboard.total = board.total
    subboard.single_form = kwargs.get('single_form')
    model.boards.append(subboard)
    ranges = [range(dim) for dim in subboard.dims]
    for entry in product(*ranges):
        new_int_var = model.NewIntVar(0, 1, "_" + repr(entry))
        subboard[entry] = new_int_var
    line_ranges_by_dims = []
    for i in range(len(subboard.dims)):
        line_ranges = copy(ranges)
        line_ranges[i] = [None]
        line_ranges_by_dims.append(line_ranges)
    lines_by_dim = [[subboard[line] for line in product(*lrs)] 
        for lrs in line_ranges_by_dims]
    subboard.magic_sums = [msum // (cell_size // cell_dims[n]) for n, msum in enumerate(board.magic_sums)]
    for dim_num, lines in enumerate(lines_by_dim):
        for line in lines:
            model.Add(sum(line) == subboard.magic_sums[dim_num])
    
    if diagonals:
        for sign in [1, -1]:
            model.Add(sum([subboard[(i, sign * i - int(sign == -1))] for i in ranges[0]]) == subboard.magic_sums[0])
    # cell constraints
    ranges = [range(dim) for dim in board.dims]
    for cell_index in product(*ranges):
        cell_ranges = [range(cell_index[i] * dim,
                            (cell_index[i] + 1) * dim) 
                            for i, dim in enumerate(cell_dims)]
        cell = [subboard[i] for i in product(*cell_ranges)]
        model.Add(sum(cell) == board[cell_index])
    # only works in 2d. Absence of kitty corners is necessary for hole-free polyominoes
    if crinkles or kitty_corners:
        for i in range(subboard.dims[0] - 1):
            for j in range(subboard.dims[1] - 1):
                corners = [subboard[(i, j)], subboard[(i+1, j)],
                           subboard[(i, j+1)], subboard[(i+1, j+1)]]
                if crinkles:
                    model.Add((sum(corners) != 2))
                if kitty_corners:
                    model.Add(sum([(2 ** i) * corner for i, corner in enumerate(corners)]) != 6)
                    model.Add(sum([(2 ** i) * corner for i, corner in enumerate(corners)]) != 9)


    # Filter out 1 unit puddles and islands
    if puddleless:
        for i in range(1, subboard.dims[0] - 1):
            for j in range(1, subboard.dims[1] - 1):
                neighbors = [subboard[(i-1, j)], subboard[(i+1, j)],
                             subboard[(i, j-1)], subboard[(i, j+1)]]
                model.Add(sum(neighbors) != 4 - 4 * subboard[(i,j)])
        # on edges, puddles are fine, but not islands
        print('subboard.dims', subboard.dims)

        for i in range(1, subboard.dims[0] - 1):
            neighbors = [subboard[(i-1, 0)], 
                         subboard[(i+1, 0)], 
                         subboard[(i, 1)]]
            model.Add(sum(neighbors) - subboard[(i, 0)] >= 0)
            neighbors = [subboard[(i-1, -1)], 
                         subboard[(i+1, -1)], 
                         subboard[(i, -2)]]
            model.Add(sum(neighbors) - subboard[(i, -1)] >= 0)
        for i in range(1, subboard.dims[1] - 1):
            neighbors = [subboard[(0, i-1)], 
                         subboard[(0, i+1)], 
                         subboard[(1, i)]]
            model.Add(sum(neighbors) - subboard[(0, i)] >= 0)
            neighbors = [subboard[(-1, i-1)], 
                         subboard[(-1, i+1)], 
                         subboard[(-2, i)]]
            model.Add(sum(neighbors) - subboard[(-1, i)] >= 0)
        
        neighbors = [subboard[(0, 1)], subboard[(1, 0)]]
        model.Add(sum(neighbors) - subboard[(0,0)] >= 0)
        neighbors = [subboard[(-1, 1)], subboard[(-2, 0)]]
        model.Add(sum(neighbors) - subboard[(-1,0)] >= 0)
        neighbors = [subboard[(1, -1)], subboard[(0, -2)]]
        model.Add(sum(neighbors) - subboard[(0,-1)] >= 0)
        neighbors = [subboard[(-2, -1)], subboard[(-1, -2)]]
        model.Add(sum(neighbors) - subboard[(-1,-1)] >= 0)
    
    if translate_swap:
        for i in range(subboard.dims[0] // 2):
            for j in range(subboard.dims[1]):
                model.Add(subboard[(i, j)] + subboard[(i + subboard.dims[0] // 2), j] == 1)

    #model.solution_printer = MetaPrinter(model.board, subboard)

