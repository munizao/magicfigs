from boards.genint import GenIntBoard
from operator import mul, eq
from functools import reduce
from ortools.sat.python import cp_model
from itertools import product
from more_itertools import collapse, all_equal
from copy import copy
from ndlist import ndlist
from solprinters import SolPrinter

class MagicBoard(GenIntBoard):
    def __init__(self, dims, min_cell=1, **kwargs):
        self.diagonals = kwargs.get('diagonals')
        super().__init__(dims, min_cell)

    def set_max_cell(self):
        self.max_cell = self.min_cell + self.cell_cnt - 1

    def setup(self):
        for entry in product(*self.ranges):
            new_int_var = self.model.NewIntVar(self.min_cell, self.max_cell, repr(entry))
            self[entry] = new_int_var
        for dim_num, lines in enumerate(self.lines()):
            for line in lines:
                self.model.Add(sum(line) == self.magic_sums[dim_num])
        if self.diagonals:
            l = len(self.dims)
            sign_lists = [[1- ((n >> i) % 2) * 2 for i in range(l)] for n in range(2 ** (l - 1))]
            for signs in sign_lists:
                indices = [[i * sign - int(sign == -1)  for sign in signs] for i in range(self.dims[0])]
                self.model.Add(sum([self[index] for index in indices]) == self.magic_sums[0])
        self.model.AddAllDifferent(collapse(self))
        self.remove_symmetries()
        self.solution_printer = SolPrinter(self)