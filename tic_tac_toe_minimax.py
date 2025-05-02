# Tic Tac Toe with Minimax Algorithm

def print_board(board):
    for row in board:
        print(" | ".join(row))
        print("-" * 9)

def is_winner(board, player):
    # Check rows, columns and diagonals for a win
    for i in range(3):
        if all([cell == player for cell in board[i]]):
            return True
        if all([board[j][i] == player for j in range(3)]):
            return True
    if all([board[i][i] == player for i in range(3)]):
        return True
    if all([board[i][2 - i] == player for i in range(3)]):
        return True
    return False

def is_board_full(board):
    return all([cell != ' ' for row in board for cell in row])

def get_available_moves(board):
    moves = []
    for i in range(3):
        for j in range(3):
            if board[i][j] == ' ':
                moves.append((i, j))
    return moves

def minimax(board, depth, is_maximizing):
    if is_winner(board, 'O'):
        return 10 - depth
    if is_winner(board, 'X'):
        return depth - 10
    if is_board_full(board):
        return 0

    if is_maximizing:
        best_score = -float('inf')
        for (i, j) in get_available_moves(board):
            board[i][j] = 'O'
            score = minimax(board, depth + 1, False)
            board[i][j] = ' '
            best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for (i, j) in get_available_moves(board):
            board[i][j] = 'X'
            score = minimax(board, depth + 1, True)
            board[i][j] = ' '
            best_score = min(score, best_score)
        return best_score

def find_best_move(board):
    best_score = -float('inf')
    best_move = None
    for (i, j) in get_available_moves(board):
        board[i][j] = 'O'
        score = minimax(board, 0, False)
        board[i][j] = ' '
        if score > best_score:
            best_score = score
            best_move = (i, j)
    return best_move

def play_game():
    board = [[' ' for _ in range(3)] for _ in range(3)]
    print("Tic Tac Toe Game: You are X, AI is O")
    print_board(board)

    while True:
        # Player move
        while True:
            try:
                move = input("Enter your move (row and column: 0 0 for top-left): ")
                i, j = map(int, move.split())
                if board[i][j] == ' ':
                    board[i][j] = 'X'
                    break
                else:
                    print("Cell already occupied, try again.")
            except (ValueError, IndexError):
                print("Invalid input, enter row and column numbers between 0 and 2.")

        print_board(board)
        if is_winner(board, 'X'):
            print("You win!")
            break
        if is_board_full(board):
            print("It's a tie!")
            break

        # AI move
        print("AI is making a move...")
        move = find_best_move(board)
        if move:
            board[move[0]][move[1]] = 'O'
        print_board(board)
        if is_winner(board, 'O'):
            print("AI wins!")
            break
        if is_board_full(board):
            print("It's a tie!")
            break

if __name__ == "__main__":
    play_game()
