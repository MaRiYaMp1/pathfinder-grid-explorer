def print_board(board):
    print("-------------")
    for i in range(3):
        print("|", board[i*3], "|", board[i*3+1], "|", board[i*3+2], "|")
        print("-------------")

def check_winner(board, player):
    for i in range(3):
        if board[i*3] == board[i*3+1] == board[i*3+2] == player:
            return True
        if board[i] == board[i+3] == board[i+6] == player:
            return True
    if board[0] == board[4] == board[8] == player:
        return True
    if board[2] == board[4] == board[6] == player:
        return True
    return False

def tic_tac_toe():
    board = [" " for _ in range(9)]
    current_player = "X"
    game_over = False

    while not game_over:
        print_board(board)
        position = int(input(f"Player {current_player}, enter your move (1-9): ")) - 1

        if board[position] == " ":
            board[position] = current_player
            if check_winner(board, current_player):
                print_board(board)
                print(f"Player {current_player} wins!")
                game_over = True
            elif " " not in board:
                print_board(board)
                print("It's a tie!")
                game_over = True
            else:
                current_player = "O" if current_player == "X" else "X"
        else:
            print("Invalid move. Try again.")

if __name__ == "__main__":
    tic_tac_toe()