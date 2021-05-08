# Add constraints that put lowest numbers in different rows, columns, and [TODO] blocks.
# Only works in squares.
from cp_sat_utils import memberOf

def lowrooks(board):
    print(board.dims, board.total)
    rooks_by_dim = [[board.model.NewIntVar(board.min_cell, board.min_cell + board.dims[dim_num] - 1, "rk" + repr(i) + ":" + repr(dim_num)) 
        for i in range(board.min_cell, board.dims[dim_num] + 1)] 
        for dim_num, dim in enumerate(board.dims)]
    for dim_num, rooks in enumerate(rooks_by_dim):
        board.model.AddAllDifferent(rooks)
        lines = board.lines()[dim_num]
        for i, rook in enumerate(rooks):
            memberOf(board.model, lines[i], rook)