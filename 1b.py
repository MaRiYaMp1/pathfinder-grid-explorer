def printSolution(board, N):
    for i in range(N):
        for j in range(N):
            if board[i][j] == 1:
                print("Q", end=" ")
            else:
                print(".", end=" ")
        print()

def isSafe(board, row, col, N):
    for i in range(col):
        if board[row][i] == 1:
            return False

    for i, j in zip(range(row, -1, -1), range(col, -1, -1)):
        if board[i][j] == 1:
            return False

    for i, j in zip(range(row, N, 1), range(col, -1, -1)):
        if board[i][j] == 1:
            return False

    return True

def solveNQUtil(board, col, N):
    if col >= N:
        return True

    for i in range(N):
        if isSafe(board, i, col, N):
            board[i][col] = 1

            if solveNQUtil(board, col + 1, N):
                return True

            board[i][col] = 0

    return False

def solveNQ(N):
    board = [[0 for _ in range(N)] for _ in range(N)]

    if not solveNQUtil(board, 0, N):
        print("Solution does not exist")
        return False

    printSolution(board, N)
    return True

if __name__ == '__main__':
    try:
        N = int(input("Enter the value of N: "))
        if N <= 0:
            print("Please enter a positive integer.")
        else:
            solveNQ(N)
    except ValueError:
        print("Invalid input. Please enter a valid integer.")
