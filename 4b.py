from collections import deque

def robot_navigation_bfs(grid, start, goal):
  rows, cols = len(grid), len(grid[0])
  if not (0 <= start[0] < rows and 0 <= start[1] < cols and
          0 <= goal[0] < rows and 0 <= goal[1] < cols and
          grid[start[0]][start[1]] == 0 and grid[goal[0]][goal[1]] == 0):
    return None  # Invalid start/goal or obstacles

  queue = deque([(start, [start])])  # Queue stores (position, path_so_far)
  visited = {start}  # Keep track of visited cells to avoid cycles

  while queue:
    (current_row, current_col), path = queue.popleft()

    if (current_row, current_col) == goal:
      return path

    # Explore valid neighboring cells
    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
      next_row, next_col = current_row + dr, current_col + dc
      if (0 <= next_row < rows and 0 <= next_col < cols and
          grid[next_row][next_col] == 0 and (next_row, next_col) not in visited):
        queue.append(((next_row, next_col), path + [(next_row, next_col)]))
        visited.add((next_row, next_col))

  return None  # No path found

# Example Usage:
grid = [
    [0, 0, 0, 0, 0],
    [0, 1, 1, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 1, 1, 1, 0],
    [0, 0, 0, 0, 0]
]
start_position = (0, 0)
goal_position = (4, 4)

path = robot_navigation_bfs(grid, start_position, goal_position)

if path:
  print("Path found:")
  for cell in path:
    print(cell)
else:
  print("No path found.")