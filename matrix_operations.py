def ones(size):
    matrix = []
    for i in range(0, size):
        vector = []
        for j in range(0, size):
            vector.append(1)
        matrix.append(vector)
    return matrix


def zeros(size):
    matrix = []
    for i in range(0, size):
        vector = []
        for j in range(0, size):
            vector.append(0)
        matrix.append(vector)
    return matrix


def eye(size):
    matrix = []
    for i in range(0, size):
        vector = []
        for j in range(0, size):
            if i != j:
                vector.append(0)
            else:
                vector.append(1)
        matrix.append(vector)
    return matrix
