class Matrix:
    def __init__(self, matrix):
        self.matrix = matrix

    def __add__(self, other):
        new_matrix = []
        for i in range(len(self.matrix)):
            new_row = []
            for j in range(len(self.matrix[i])):
                new_row.append(self.matrix[i][j] + other.matrix[i][j])
            new_matrix.append(new_row)
        return Matrix(new_matrix)

    def __sub__(self, other):
        new_matrix = []
        for i in range(len(self.matrix)):
            new_row = []
            for j in range(len(self.matrix[i])):
                new_row.append(self.matrix[i][j] - other.matrix[i][j])
            new_matrix.append(new_row)
        return Matrix(new_matrix)

    def __mul__(self, other):
        new_matrix = []
        for i in range(len(self.matrix)):
            new_row = []
            for j in range(len(other.matrix[0])):
                sum = 0
                for k in range(len(self.matrix[0])):
                    sum += self.matrix[i][k] * other.matrix[k][j]
                new_row.append(sum)
            new_matrix.append(new_row)
        return Matrix(new_matrix)

    def __str__(self):
        string = ""
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[i])):
                string += str(self.matrix[i][j]) + " "
            string += "\n"
        return string


def ones(size):
    matrix = []
    for i in range(0, size):
        vector = []
        for j in range(0, size):
            vector.append(1)
        matrix.append(vector)
    return Matrix(matrix)


def zeros(size):
    matrix = []
    for i in range(0, size):
        vector = []
        for j in range(0, size):
            vector.append(0)
        matrix.append(vector)
    return Matrix(matrix)


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
    return Matrix(matrix)
