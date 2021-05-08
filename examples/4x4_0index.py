import sys
sys.path.append('./')

from transforms.metaify import metaify
from boards.magic import MagicBoard

# Zero-indexed 4×4 magic squares can be used as a basis for sparse squares where 
# each number in the original square corresponds to a 3×5 cell in the corresponding 
# sparse square.

board = MagicBoard((4, 4), min_cell=0, diagonals=True)
metaify(board, (3, 5), kitty_corners=True, puddleless=True, single_form=True)
board.model.solve()