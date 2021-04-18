from ortools.sat.python import cp_model
from solprinters import SolPrinter

class Model(cp_model.CpModel):
    def __init__(self):
        self.boards = []
        super().__init__()
    def solve(self, **kwargs):
        solution_printer = SolPrinter(self.boards)
        # show_solutions = kwargs.get('show_solutions')
        solver = cp_model.CpSolver()
        status = solver.SearchForAllSolutions(self, solution_printer)
        print(solver.StatusName(status))