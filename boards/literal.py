from ndlist import ndlist
from model import Model
class LiteralBoard(ndlist):
    def __init__(self, l):
        self.model = Model()
        self.model.boards.append(self)
        self.total = sum([sum(m) for m in l])
        self.type = int
        # fix if I ever go to more than 3 dimensions.
        dims = (len(l[0]), len(l))
        super().__init__(dims, l)
        self.magic_sums = (sum(l[0]), sum([m[0] for m in l]))