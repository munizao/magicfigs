from metaify import metaify
from magic import MagicModel

model = MagicModel((3, 3), diagonals=True)
metaify(model, (3, 3), diagonals=True, kitty_corners=True, puddleless=True, single_form=True)
model.solve()