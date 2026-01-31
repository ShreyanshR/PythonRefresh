from typing import List

class NumMatrix:

    def __init__(self, matrix: List[List[int]]):
        if not matrix or not matrix[0]:
            return
            
        ROWS, COLS = len(matrix), len(matrix[0])
        self.sumMatrix = [[0] * (COLS + 1) for r in range(ROWS+1)]

        for r in range(ROWS):
            prefix = 0
            for c in range(COLS):
                prefix += matrix[r][c]
                above = self.sumMatrix[r][c+1]
                self.sumMatrix[r+1][c+1] = prefix + above
        print(self.sumMatrix)
        
    def sumRegion(self, row1: int, col1: int, row2: int, col2: int) -> int:
        r1, c1, r2, c2 = row1, col1, row2, col2
        return (self.sumMatrix[r2 + 1][c2 + 1] - 
                self.sumMatrix[r1][c2 + 1] - 
                self.sumMatrix[r2 + 1][c1] + 
                self.sumMatrix[r1][c1])


if __name__ == "__main__":
    matrix = [
        [3, 0, 1], 
        [5, 6, 3], 
        [1, 2, 0]
    ]

    sol = NumMatrix(matrix)
    print(sol.sumRegion(1,1,2,2))
