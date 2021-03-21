from ndlist import ndlist

l = ndlist.empty((2,3,4))
print(l)
print(l.dims)
row = l[None, 1, 0]
print(row)

m = ndlist([[1,2], [3,4]], (2,2))
print(m)
