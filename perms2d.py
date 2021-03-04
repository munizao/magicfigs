from itertools import permutations

def transpose(matrix):
    return [[row[i] for row in matrix] for i in range(len(matrix[0]))]

def permutations_2d(matrix):
    for p1 in permutations(matrix):
        t = transpose(p1)
        for p2 in permutations(t):
            yield transpose(p2)
