from metaify import metaify
from latin import LatinModel

model = LatinModel((5, 5), min_cell=0)
metaify(model, (2, 2), kitty_corners=True, puddleless=True, single_form=True, diagonals=True)
model.solve()