import sys
sys.path.append('./')
from boards.sparse import SparseModel

model = SparseModel(12, 4, syms='d')
model.solve()