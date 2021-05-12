# Add constraints that put lowest numbers in different rows, columns, and [TODO] blocks.
# Only works in squares.
from cp_sat_utils import memberOf

def lowrooks(board, **kwargs):
    #queens seem a bit harder than rooks, shelving for now.
    #diagonals = kwargs.get('diagonals')
    rooks_by_dim = [[board.model.NewIntVar(board.min_cell, board.min_cell + board.dims[dim_num] - 1, "rk" + repr(i) + ":" + repr(dim_num)) 
        for i in range(board.min_cell, board.dims[dim_num] + 1)] 
        for dim_num in range(board.dims)]
    for dim_num, rooks in enumerate(rooks_by_dim):
        lines = board.lines()[dim_num]
        for i, rook in enumerate(rooks):
            memberOf(board.model, lines[i], rook)