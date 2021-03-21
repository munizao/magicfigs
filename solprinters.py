from ortools.sat.python import cp_model
from more_itertools import collapse

class IntPrinter(cp_model.CpSolverSolutionCallback):
    def __init__(self, board, int_width=2):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.board = board
        self.int_width = int_width
    
    def print_board(self, board, dim_num):
        if dim_num >= 3:
            print('-' * dim_num)
            for subboard in board:
                self.print_board(subboard, dim_num - 1)
        else:
            print('--')
            for line in board:
                for entry in line:
                    print('{0:{width}}'.format(self.Value(entry), width=self.int_width),
                        end=" ")
                print()
            
    def OnSolutionCallback(self):
        self.print_board(self.board, len(self.board.dims))