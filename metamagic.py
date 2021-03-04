from ortools.sat.python import cp_model

def model_metamagic(meta_board, magic_sum, cell_dims, options={}):
    diagonals = options.get('diagonals')
    kitty_corners = options.get('kitty_corners')
    meta_dims = (len(meta_board[0]), len(meta_board))
    board_dims = [meta_dims[i] * cell_dims[i] for i in (0, 1)]

    # break symmetry
    if meta_board[0][0] > meta_board[0][meta_dims[0] - 1]:
        return (None, None)

    if meta_board[0][0] < meta_board[meta_dims[1] - 1][0]:
        return (None, None)

    model = cp_model.CpModel()
    board = [[model.NewIntVar(0, 1, repr([i, j])) for i in range(board_dims[0])]
             for j in range(board_dims[1])]
    board_cols = [[board[i][j] for i in range(board_dims[1])] for j in range(board_dims[0])]

    # row and column sum to divisor of magic sum
    for i in range(board_dims[0]):
        model.Add(sum(board[i]) == magic_sum // cell_dims[1])
    for i in range(board_dims[1]):
        model.Add(sum(board_cols[i]) == magic_sum // cell_dims[0])

    if diagonals:
        if board_dims[0] != board_dims[1]:
            print('Board is non-square, diagonal constraints disabled')
        else:
            model.Add(sum([board[i][i] for i in range(board_dims[0])])
                      == magic_sum // cell_dims[0])
            model.Add(sum([board[i][-i] for i in range(board_dims[0])])
                      == magic_sum // cell_dims[0])

    # cells sum to meta-board entry
    for i in range(meta_dims[0]):
        for j in range(meta_dims[1]):
            model.Add(sum([board[x][y]
                          for x in range(cell_dims[0] * i, cell_dims[0] * (i + 1))
                          for y in range(cell_dims[1] * j, cell_dims[1] * (j + 1))])
                      == meta_board[i][j])

    if kitty_corners:
        for i in range(board_dims[0] - 1):
            for j in range(board_dims[1] - 1):
                model.Add((board[i][j] + board[i+1][j+1] + board[i+1][j] + board[i][j+1] != 2) or
                          (board[i][j] + board[i+1][j+1] != 2) and
                          (board[i][j] + board[i+1][j+1] != 0))

    return model, board


class SolutionPrinter(cp_model.CpSolverSolutionCallback):
    def __init__(self, board):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.board = board

    def OnSolutionCallback(self):
        for row in self.board:
            [print('░', end='') if self.Value(i) else print('█', end='') for i in row]
            print()
        print()


def solve_metamagic(meta_board, magic_sum, cell_dims, options):
    solver = cp_model.CpSolver()
    model, board = model_metamagic(meta_board, magic_sum, cell_dims, options)
    if model:
        solution_printer = SolutionPrinter(board)
        status = solver.SearchForAllSolutions(model, solution_printer)
        print(status)
