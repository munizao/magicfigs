from ortools.sat.python import cp_model
from more_itertools import collapse

class SolPrinter(cp_model.CpSolverSolutionCallback):
    def __init__(self, board, type=int, int_width=2):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.board = board
        self.type = type
        self.int_width = int_width
    
    def print_board(self, board, dim_num, type):
        if dim_num >= 3:
            print('-' * dim_num)
            for subboard in board:
                self.print_board(subboard, dim_num - 1, type)
        else:
            print('--')
            for line in board:
                for entry in line:
                    if type == int:
                        print('{0:{width}}'.format(self.Value(entry), width=self.int_width), 
                        end=" ")
                    elif type == bool:
                        print('█', end='') if self.Value(entry) else print('░', end='')
                print()
            
    def OnSolutionCallback(self):
        self.print_board(self.board, len(self.board.dims), self.type)

class MetaPrinter(SolPrinter):
    def __init__(self, board, subboard, type=int, int_width=2):
        super().__init__(board, type, int_width)
        self.subboard = subboard
    def OnSolutionCallback(self):
        self.print_board(self.board, len(self.board.dims), int)
        self.print_board(self.subboard, len(self.board.dims), bool)