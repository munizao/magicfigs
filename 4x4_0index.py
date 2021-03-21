from metaify import metaify
from magic import MagicModel

# Zero-indexed 4×4 magic squares can be used as a basis for sparse squares where 
# each number in the original square corresponds to a 3×5 cell in the corresponding 
# sparse square.

model = MagicModel((4, 4), min_cell=0)
metaify(model, (3, 5))
model.solve()