m = [
  [1,   4,  7, 11, 15],
  [2,   5,  8, 12, 19],
  [3,   6,  9, 16, 22],
  [10, 13, 14, 17, 24],
  [18, 21, 23, 26, 30]
]


def findNumberIn2DArray(matrix, target):
    i = int(len(matrix) / 2)
    j = int(len(matrix[0]) / 2)
    width = int(len(matrix) / 2)

    while matrix[i][j] > target:
        while i >= 0:
            while j >= 0:
                if matrix[i][j] == target:
                    return matrix[i][j]
                j -= 1
            j = width
            i -= 1

    while matrix[i][j] < target:
        i += i / 2
        j += j / 2
        i = int(i)
        j = int(j)
        if matrix[i][j] >= target:
            return matrix[i][j]
    return matrix[i][j]
m = findNumberIn2DArray(m,11)
print(m)