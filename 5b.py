import heapq
import math

class RobotState:
    def __init__(self, position, parent=None, action=None):
        self.position = position
        self.parent = parent
        self.action = action
        self.g = 0  # cost from start
        if parent:
            self.g = parent.g + 1

    def __eq__(self, other):
        return self.position == other.position

    def __lt__(self, other):
        return (self.g + self.heuristic()) < (other.g + other.heuristic())

    def __hash__(self):
        return hash(self.position)

    def heuristic(self, goal_position):
        # Euclidean distance heuristic
        return math.sqrt((self.position[0] - goal_position[0])**2 + 
                        (self.position[1] - goal_position[1])**2)

    def get_successors(self, grid):
        successors = []
        rows, cols = len(grid), len(grid[0])
        x, y = self.position
        moves = [(-1, 0, 'Up'), (1, 0, 'Down'), (0, -1, 'Left'), (0, 1, 'Right')]

        for dx, dy, action in moves:
            nx, ny = x + dx, y + dy
            if 0 <= nx < rows and 0 <= ny < cols and grid[nx][ny] != 1:
                successors.append(RobotState((nx, ny), self, action))
        return successors

def a_star_robot(grid, start, goal):
    open_list = []
    closed_set = set()
    start_state = RobotState(start)
    heapq.heappush(open_list, (start_state.g + start_state.heuristic(goal), start_state))
    
    while open_list:
        _, current = heapq.heappop(open_list)
        
        if current.position == goal:
            path = []
            while current.parent:
                path.append(current.action)
                current = current.parent
            return path[::-1]
        
        closed_set.add(current)
        
        for successor in current.get_successors(grid):
            if successor not in closed_set:
                heapq.heappush(open_list, 
                             (successor.g + successor.heuristic(goal), successor))
    
    return None

# Example usage
grid = [
    [0, 0, 0, 0, 1],
    [1, 1, 0, 1, 0],
    [0, 0, 0, 0, 0],
    [0, 1, 1, 1, 0],
    [0, 0, 0, 0, 0]
]
start = (0, 0)
goal = (4, 4)
print("Robot Navigation Solution:", a_star_robot(grid, start, goal))
