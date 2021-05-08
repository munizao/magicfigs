import sys
sys.path.append('./')
from boards.magic import MagicBoard
from transforms.lowrooks import lowrooks

board = MagicBoard((4, 4), diagonals=True)
lowrooks(board)
board.model.solve()