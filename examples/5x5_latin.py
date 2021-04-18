import sys
sys.path.append('./')
from metaify import metaify
from boards.latin import LatinBoard

board = LatinBoard((5, 5), min_cell=0)
metaify(board, (2, 2), kitty_corners=True, puddleless=True, single_form=True, diagonals=True)
board.model.solve()