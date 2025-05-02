import heapq

class NPuzzleState:
    def __init__(self, board, parent=None, move=""):
        self.board = [row[:] for row in board]
        self.parent = parent
        self.move = move
        self.g = 0  # cost from start
        if parent:
            self.g = parent.g + 1

    def __eq__(self, other):
        return self.board == other.board

    def __lt__(self, other):
        return (self.g + self.heuristic()) < (other.g + other.heuristic())

    def __hash__(self):
        return hash(tuple(tuple(row) for row in self.board))

    def find_blank(self):
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                if self.board[i][j] == 0:
                    return i, j

    def heuristic(self):
        # Manhattan distance heuristic
        distance = 0
        n = len(self.board)
        for i in range(n):
            for j in range(n):
                if self.board[i][j] != 0:
                    x, y = divmod(self.board[i][j] - 1, n)
                    distance += abs(x - i) + abs(y - j)
        return distance

    def get_successors(self):
        successors = []
        i, j = self.find_blank()
        moves = [(0, 1, 'Right'), (0, -1, 'Left'), (1, 0, 'Down'), (-1, 0, 'Up')]

        for di, dj, move in moves:
            ni, nj = i + di, j + dj
            if 0 <= ni < len(self.board) and 0 <= nj < len(self.board[0]):
                new_board = [row[:] for row in self.board]
                new_board[i][j], new_board[ni][nj] = new_board[ni][nj], new_board[i][j]
                successors.append(NPuzzleState(new_board, self, move))
        return successors

def a_star_npuzzle(initial_board, goal_board):
    initial_state = NPuzzleState(initial_board)
    goal_state = NPuzzleState(goal_board)
    
    open_list = []
    closed_set = set()
    heapq.heappush(open_list, (initial_state.g + initial_state.heuristic(), initial_state))
    
    while open_list:
        _, current = heapq.heappop(open_list)
        
        if current.board == goal_state.board:
            path = []
            while current.parent:
                path.append(current.move)
                current = current.parent
            return path[::-1]
        
        closed_set.add(current)
        
        for successor in current.get_successors():
            if successor not in closed_set:
                heapq.heappush(open_list, (successor.g + successor.heuristic(), successor))
    
    return None

# Example usage for 8-puzzle (3x3)
initial = [[1, 2, 3], [0, 4, 6], [7, 5, 8]]
goal = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
print("N-Puzzle Solution:", a_star_npuzzle(initial, goal))
