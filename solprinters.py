from ndlist import ndlist
from ortools.sat.python import cp_model
from more_itertools import collapse
from copy import copy

class SolPrinter(cp_model.CpSolverSolutionCallback):
    def __init__(self, boards, type=int, int_width=2):
        cp_model.CpSolverSolutionCallback.__init__(self)
        if isinstance(boards, ndlist):
            self.boards = [boards]
        else:
            self.boards = boards
        self.type = type
        self.int_width = int_width
        self.count = 0
    
    def print_board(self, board, type=None):
        if type is None:
            type = board.type
        dim_num = len(board.dims)
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
        do_print = True
        for board in self.boards:
            if getattr(board, 'single_form', None):
                visited = set()
                unvisited = set()
                for i in range(board.dims[0]):
                    index = [0 for _ in board.dims]
                    index[0] = i
                    if self.Value(board[index]) == 1:
                        unvisited.add(tuple(index))
                        break
                
                while unvisited:
                    to_visit = unvisited.pop()
                    for i, dim in enumerate(board.dims):
                        for sign in [-1, 1]:
                            if 0 <= to_visit[i] + sign < dim: 
                                new_index = list(to_visit)
                                new_index[i] += sign
                                new_index = tuple(new_index)
                                if not new_index in visited: 
                                    if self.Value(board[new_index]):
                                        unvisited.add(new_index)
                    visited.add(to_visit)
                if len(visited) < board.total:
                    do_print = False
        if do_print:
            for board in self.boards:
                self.print_board(board)
            self.count += 1
            print(self.count)

# class MetaPrinter(SolPrinter):
#     def __init__(self, board, subboard, type=int, int_width=2):
#         super().__init__(board, type, int_width)
#         self.subboard = subboard
#         self.count = 0
#     def OnSolutionCallback(self):
#         do_print = True
#         if self.subboard.single_form:
#             visited = set()
#             unvisited = set()
#             for i in range(self.subboard.dims[0]):
#                 index = [0 for _ in self.subboard.dims]
#                 index[0] = i
#                 if self.Value(self.subboard[index]) == 1:
#                     unvisited.add(tuple(index))
#                     break
            
#             while unvisited:
#                 to_visit = unvisited.pop()
#                 for i, dim in enumerate(self.subboard.dims):
#                     for sign in [-1, 1]:
#                         if 0 <= to_visit[i] + sign < dim: 
#                             new_index = list(to_visit)
#                             new_index[i] += sign
#                             new_index = tuple(new_index)
#                             if not new_index in visited: 
#                                 if self.Value(self.subboard[new_index]):
#                                     unvisited.add(new_index)
#                 visited.add(to_visit)
#             if len(visited) < self.board.total:
#                 do_print = False
#         if do_print:
#             self.count += 1
#             self.print_board(self.board, len(self.board.dims), int)
#             self.print_board(self.subboard, len(self.board.dims), bool)
#             print(self.count)
