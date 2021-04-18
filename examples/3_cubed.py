import sys
sys.path.append('./')
from boards.magic import MagicBoard

board = MagicBoard((3,3,3), diagonals=True)
board.model.solve()