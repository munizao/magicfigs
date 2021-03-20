# Quick and dirty n-dimensional list. Didn't want to import numpy.

from itertools import product

class ndlist(list):
    @classmethod
    def empty(cls, dims):
        newlist = []
        for cell in product(*[range(dim) for dim in dims]):
            sublist = newlist
            for i, coord in enumerate(cell):
                if i < len(cell) - 1:
                    if coord == 0:
                        sublist.append([])
                    sublist = sublist[coord]
                else:
                    sublist.append(None)
        cls.__new__(newlist)

    def __getitem__(self, index):
        if iter(index):
            sublist = self
            for subindex in index:
                sublist = sublist[subindex]
            return sublist
        return super().__getitem__(index)
    
    def __setitem__(self, index, newval):
        if iter(index):
            sublist = self
            for i, subindex in enumerate(index):
                sublist = sublist[subindex]
                if i == len(index) - 1:
                    sublist[subindex] = newval
        else:
            super().__setitem__(index, newval)