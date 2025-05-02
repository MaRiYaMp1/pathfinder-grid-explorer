import heapq

class PuzzleState:
    def __init__(self, board, parent=None, move=""):
        self.board = [row[:] for row in board]
        self.parent = parent
        self.move = move
        self.depth = 0
        if parent:
            self.depth = parent.depth + 1

    def __eq__(self, other):
        return self.board == other.board

    def __lt__(self, other):
        return self.heuristic() < other.heuristic()

    def __hash__(self):
        return hash(tuple(tuple(row) for row in self.board))

    def __str__(self):
        return '\n'.join([' '.join(map(str, row)) for row in self.board])

    def find_blank(self):
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == 0:
                    return i, j

    def heuristic(self):
        # Manhattan distance heuristic
        distance = 0
        for i in range(3):
            for j in range(3):
                if self.board[i][j] != 0:
                    x, y = divmod(self.board[i][j] - 1, 3)
                    distance += abs(x - i) + abs(y - j)
        return distance

    def get_successors(self):
        successors = []
        i, j = self.find_blank()
        moves = [(0, 1, 'Right'), (0, -1, 'Left'), (1, 0, 'Down'), (-1, 0, 'Up')]

        for di, dj, move in moves:
            ni, nj = i + di, j + dj
            if 0 <= ni < 3 and 0 <= nj < 3:
                new_board = [row[:] for row in self.board]
                new_board[i][j], new_board[ni][nj] = new_board[ni][nj], new_board[i][j]
                successors.append(PuzzleState(new_board, self, move))
        return successors

    def is_goal(self, goal_board):
        return self.board == goal_board

def best_first_search(initial_board, goal_board):
    initial_state = PuzzleState(initial_board)
    goal_state = PuzzleState(goal_board)
    
    open_list = []
    closed_set = set()
    heapq.heappush(open_list, (initial_state.heuristic(), initial_state))
    
    while open_list:
        _, current = heapq.heappop(open_list)
        
        if current.is_goal(goal_board):
            path = []
            while current.parent:
                path.append(current.move)
                current = current.parent
            return path[::-1]
        
        closed_set.add(current)
        
        for successor in current.get_successors():
            if successor not in closed_set:
                heapq.heappush(open_list, (successor.heuristic(), successor))
    
    return None  # No solution found

def get_puzzle_input(prompt):
    print(prompt)
    board = []
    for i in range(3):
        while True:
            row_str = input(f"Enter row {i+1} (3 numbers separated by spaces, 0 for blank): ")
            try:
                row = list(map(int, row_str.split()))
                if len(row) != 3:
                    raise ValueError
                board.append(row)
                break
            except ValueError:
                print("Invalid input. Please enter 3 numbers separated by spaces.")
    return board

def main():
    print("8-Puzzle Solver using Best-First Search")
    print("Enter the initial state:")
    initial_board = get_puzzle_input("Enter the initial board (0 represents the blank space):")
    
    print("\nEnter the goal state:")
    goal_board = get_puzzle_input("Enter the goal board (0 represents the blank space):")
    
    solution = best_first_search(initial_board, goal_board)
    
    if solution:
        print("\nSolution found in", len(solution), "moves:")
        print(" -> ".join(solution))
    else:
        print("\nNo solution found!")

if __name__ == "__main__":
    main()
