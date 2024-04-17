
def generate_4sudoku():
    """
    生成一个4x4数独， 返回一个数组， 0表示空位
    """
    sudoku = [[0 for _ in range(4)] for _ in range(4)]
    for i in range(4):
        for j in range(4):
            sudoku[i][j] = (i * 2 + i // 2 + j) % 4 + 1
    return sudoku


def solve_4sudoku(sudoku):
    """
    解4x4数独，返回解
    """
    def is_valid(sudoku, row, col, num):
        for i in range(4):
            if sudoku[row][i] == num or sudoku[i][col] == num:
                return False
        start_row, start_col = row - row % 2, col - col % 2
        for i in range(2):
            for j in range(2):
                if sudoku[i + start_row][j + start_col] == num:
                    return False
        return True

    def solve(sudoku):
        for i in range(4):
            for j in range(4):
                if sudoku[i][j] == 0:
                    for num in range(1, 5):
                        if is_valid(sudoku, i, j, num):
                            sudoku[i][j] = num
                            if solve(sudoku):
                                return True
                            sudoku[i][j] = 0
                    return False
        return True

    solve(sudoku)
    return sudoku