# Quick and dirty n-dimensional list. Didn't want to import numpy.

from itertools import product
from copy import copy, deepcopy
from collections.abc import Iterable

class ndlist(list):

    def __init__(self, dims, l=None):
        self.dims = dims
        self.ranges = [range(dim) for dim in self.dims]
        if not isinstance(l, Iterable):
            for dim in dims[::-1]:
                l = [deepcopy(l) for _ in range(dim)]
        super().__init__(l)

    # @classmethod
    # def empty(cls, dims):
    #     newlist = None
    #     for dim in dims[::-1]:
    #         newlist = [deepcopy(newlist) for _ in range(dim)]
    #     newlist = cls(dims, newlist)
    #     return newlist

    def __getitem__(self, index):
        if isinstance(index, Iterable):
            if None in index:
                # print("index:", index)
                dim_num = index.index(None)
                row = []
                for i in range(self.dims[dim_num]):
                    entry_index = list(index)
                    entry_index[dim_num] = i
                    # print("entry_index", entry_index)
                    row.append(self[entry_index])
                return row
            sublist = self
            for subindex in index:
                sublist = sublist[subindex]
            return sublist
        return super().__getitem__(index)
    
    def __setitem__(self, index, newval):
        if iter(index):
            sublist = self
            for i, subindex in enumerate(index):
                # print("sublist:", sublist, "i:", i, "index:", index)
                if i == len(index) - 1:
                    sublist[subindex] = newval
                sublist = sublist[subindex]
        else:
            super().__setitem__(index, newval)
    
    def lines(self):
        line_ranges_by_dims = []
        for i in range(len(self.dims)):
            line_ranges = copy(self.ranges)
            line_ranges[i] = [None]
            line_ranges_by_dims.append(line_ranges)
        return [[self[line] for line in product(*lrs)] for lrs in line_ranges_by_dims]