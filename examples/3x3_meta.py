import sys
sys.path.append('./')

from metaify import metaify
from boards.magic import MagicBoard

board = MagicBoard((3, 3), diagonals=True)
metaify(board, (3, 3), diagonals=True, kitty_corners=True, puddleless=True, single_form=True)
board.model.solve()