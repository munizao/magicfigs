import sys
sys.path.append('./')

from metaify import metaify
from magicify import magicify
from boards.magic import MagicBoard

board = MagicBoard((3, 3), diagonals=True)
metaify(board, (3, 3), diagonals=True, kitty_corners=True, puddleless=True, single_form=True)
magicify(board)
board.model.solve()