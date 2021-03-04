from perms2d import permutations_2d
from metamagic import solve_metamagic

meta_board_proto = [
    [6, 3, 8, 1],
    [4, 6, 3, 5],
    [1, 7, 2, 8],
    [7, 2, 5, 4],
]

for meta_board in permutations_2d(meta_board_proto):
    solve_metamagic(meta_board, 18, (3, 3), {'kitty_corners': True})
