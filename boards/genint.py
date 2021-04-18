from operator import mul
from functools import reduce
from itertools import product
from more_itertools import all_equal
from copy import copy
from model import Model
from ndlist import ndlist

class GenIntBoard(ndlist):
    def __init__(self, dims, min_cell=1, **kwargs):
        self.type = int
        self.dims = dims
        self.min_cell = min_cell
        self.cell_cnt = reduce(mul, self.dims, 1)
        self.set_max_cell()
        twice_mean = self.min_cell + self.max_cell
        # if twice_mean is odd, and a board_dim is odd, it's not gonna work
        self.magic_sums = [twice_mean * dim // 2 for dim in self.dims]
        self.total = twice_mean * self.cell_cnt // 2
        self.model = Model()
        self.model.boards.append(self)
        super().__init__(dims)
        self.setup()
    
    def setup(self):
        for entry in product(*self.board.ranges):
            new_int_var = self.model.NewIntVar(self.min_cell, self.max_cell, repr(entry))
            self[entry] = new_int_var
    
    def remove_symmetries(self):
        # (Probably still broken when only some dims are equal.)
        origin = [0 for _ in self.dims]
        for i in range(1, 2 ** len(self.dims)):
            corner = [(self.dims[n] - 1) * ((i >> n) % 2) for n in range(len(self.dims))]
            self.model.Add(self[origin] <= self[corner])
        if all_equal(self.dims):
            for i, dim in enumerate(self.dims):
                corner = copy(origin)
                corner[i] = dim - 1
                if i == 0:
                    first_corner = corner
                    continue
                self.model.Add(self[first_corner] <= self[corner])