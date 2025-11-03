A_i = [
    [1, 3, 2, 1],
    [-1, 2, 5, 2],
    [1, -3, -2, -1],
    [-2, -6, -4, -2]
]
bi = [3, 5, 2, 4]

A_j = [
    [2, 1, -1, 1],
    [1, 3, 2, -1],
    [3, 2, 1, 2],
    [1, 1, 1, 1]
]
bj = [1, 4, 3, 2]

A_k = [
    [1, 2, 3, 4],
    [2, 4, 6, 8],
    [1, 1, 1, 1],
    [3, 5, 7, 9]
]
bk = [10, 20, 4, 24]

def gauss(matrix_A, bi):
    
    if matrix_A[0][0] == 0:
        for i in range(len(matrix_A[0]) - 1):
            if matrix_A[i + 1] != 0:
                new_matrix = matrix_A
                new_matrix[0] = matrix_A[i + 1]
                new_matrix[i + 1] = matrix_A[0]
        else:
            print("change column")

    for i in range(len(matrix_A)):
        for j in range(len(matrix_A[0])):
            print(matrix_A[i][j], end='')

        print()

gauss(A_k, bk)