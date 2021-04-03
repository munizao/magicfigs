from ortools.sat.python import cp_model
from itertools import product
from more_itertools import all_equal
from functools import reduce
from operator import mul
from copy import copy
from ndlist import ndlist
from solprinters import MetaPrinter

def metaify(model, cell_dims, **kwargs):
    diagonals = kwargs.get('diagonals')
    kitty_corners = kwargs.get('kitty_corners')
    puddleless = kwargs.get('puddleless')
    crinkles = kwargs.get('crinkles')
    translate_swap = kwargs.get('translate_swap')
    cell_size = reduce(mul, cell_dims, 1)
    subboard_dims = [model.dims[i] * cell_dims[i] for i in range(len(model.dims))]
    model.subboard = ndlist.empty(subboard_dims)
    model.subboard.single_form = kwargs.get('single_form')
    ranges = [range(dim) for dim in subboard_dims]
    for entry in product(*ranges):
        new_int_var = model.NewIntVar(0, 1, "_" + repr(entry))
        model.subboard[entry] = new_int_var
    line_ranges_by_dims = []
    for i in range(len(subboard_dims)):
        line_ranges = copy(ranges)
        line_ranges[i] = [None]
        line_ranges_by_dims.append(line_ranges)
    lines_by_dim = [[model.subboard[line] for line in product(*lrs)] 
        for lrs in line_ranges_by_dims]
    model.subboard.magic_sums = [msum // (cell_size // cell_dims[n]) for n, msum in enumerate(model.magic_sums)]
    for dim_num, lines in enumerate(lines_by_dim):
        for line in lines:
            model.Add(sum(line) == model.subboard.magic_sums[dim_num])
    
    if diagonals:
        for sign in [1, -1]:
            model.Add(sum([model.subboard[(i, sign * i - int(sign == -1))] for i in ranges[0]]) == model.subboard.magic_sums[0])
    # cell constraints
    ranges = [range(dim) for dim in model.board.dims]
    for cell_index in product(*ranges):
        cell_ranges = [range(cell_index[i] * dim,
                            (cell_index[i] + 1) * dim) 
                            for i, dim in enumerate(cell_dims)]
        cell = [model.subboard[i] for i in product(*cell_ranges)]
        model.Add(sum(cell) == model.board[cell_index])
    # only works in 2d. Absence of kitty corners is necessary for hole-free polyominoes
    if crinkles or kitty_corners:
        for i in range(subboard_dims[0] - 1):
            for j in range(subboard_dims[1] - 1):
                corners = [model.subboard[(i, j)], model.subboard[(i+1, j)],
                           model.subboard[(i, j+1)], model.subboard[(i+1, j+1)]]
                if crinkles:
                    model.Add((sum(corners) != 2))
                if kitty_corners:
                    model.Add(sum([(2 ** i) * corner for i, corner in enumerate(corners)]) != 6)
                    model.Add(sum([(2 ** i) * corner for i, corner in enumerate(corners)]) != 9)


    # Filter out 1 unit puddles and islands
    if puddleless:
        for i in range(1, subboard_dims[0] - 1):
            for j in range(1, subboard_dims[1] - 1):
                neighbors = [model.subboard[(i-1, j)], model.subboard[(i+1, j)],
                             model.subboard[(i, j-1)], model.subboard[(i, j+1)]]
                model.Add(sum(neighbors) != 4 - 4 * model.subboard[(i,j)])
        # on edges, puddles are fine, but not islands
        print('subboard_dims', subboard_dims)

        for i in range(1, subboard_dims[0] - 1):
            neighbors = [model.subboard[(i-1, 0)], 
                         model.subboard[(i+1, 0)], 
                         model.subboard[(i, 1)]]
            model.Add(sum(neighbors) - model.subboard[(i, 0)] >= 0)
            neighbors = [model.subboard[(i-1, -1)], 
                         model.subboard[(i+1, -1)], 
                         model.subboard[(i, -2)]]
            model.Add(sum(neighbors) - model.subboard[(i, -1)] >= 0)
        for i in range(1, subboard_dims[1] - 1):
            neighbors = [model.subboard[(0, i-1)], 
                         model.subboard[(0, i+1)], 
                         model.subboard[(1, i)]]
            model.Add(sum(neighbors) - model.subboard[(0, i)] >= 0)
            neighbors = [model.subboard[(-1, i-1)], 
                         model.subboard[(-1, i+1)], 
                         model.subboard[(-2, i)]]
            model.Add(sum(neighbors) - model.subboard[(-1, i)] >= 0)
        
        neighbors = [model.subboard[(0, 1)], model.subboard[(1, 0)]]
        model.Add(sum(neighbors) - model.subboard[(0,0)] >= 0)
        neighbors = [model.subboard[(-1, 1)], model.subboard[(-2, 0)]]
        model.Add(sum(neighbors) - model.subboard[(-1,0)] >= 0)
        neighbors = [model.subboard[(1, -1)], model.subboard[(0, -2)]]
        model.Add(sum(neighbors) - model.subboard[(0,-1)] >= 0)
        neighbors = [model.subboard[(-2, -1)], model.subboard[(-1, -2)]]
        model.Add(sum(neighbors) - model.subboard[(-1,-1)] >= 0)
    
    if translate_swap:
        for i in range(subboard_dims[0] // 2):
            for j in range(subboard_dims[1]):
                model.Add(model.subboard[(i, j)] + model.subboard[(i + subboard_dims[0] // 2), j] == 1)

    model.solution_printer = MetaPrinter(model.board, model.subboard)

