import sys
sys.path.append('./')

from perms2d import permutations_2d
from metamagic import solve_metamagic
from boards.literal import LiteralBoard
from metaify import metaify

meta_board_proto = LiteralBoard([
    [6, 3, 8, 1],
    [4, 6, 3, 5],
    [1, 7, 2, 8],
    [7, 2, 5, 4],
])

metaify(meta_board_proto, (3, 3), kitty_corners=True, puddleless=True, diagonals=True, single_form=True)
meta_board_proto.model.solve()

# Uncomment to get solutions for other board permutations, but the above has plenty
# for meta_board in permutations_2d(meta_board_proto):
#     metaify(meta_board, (3, 3), kitty_corners=True, single_form=True)
#     meta_board.model.solve()
