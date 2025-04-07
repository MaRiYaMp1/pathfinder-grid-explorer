
import { CellType } from "@/components/GridCell";

export interface Position {
  x: number;
  y: number;
}

export interface Node {
  position: Position;
  parent: Node | null;
  depth: number;
}

// Directions: up, right, down, left
const dx = [0, 1, 0, -1];
const dy = [-1, 0, 1, 0];

// Check if a position is valid (inside grid and not a wall)
export const isValidPosition = (
  grid: CellType[][],
  position: Position
): boolean => {
  const { x, y } = position;
  return (
    x >= 0 &&
    y >= 0 &&
    x < grid[0].length &&
    y < grid.length &&
    grid[y][x] !== 'wall'
  );
};

// Depth-Limited Search (DLS) - a helper function for IDDFS
export const depthLimitedSearch = (
  grid: CellType[][],
  start: Position,
  goal: Position,
  maxDepth: number,
  visitCallback: (position: Position) => void
): Node | null => {
  // Create a visited set to avoid loops
  const visited = new Set<string>();
  
  // Create a stack for DFS
  const stack: Node[] = [{ position: start, parent: null, depth: 0 }];
  
  while (stack.length > 0) {
    const node = stack.pop()!;
    const { position, depth } = node;
    const { x, y } = position;
    
    // Skip if out of bounds or already visited or exceeds depth limit
    const posKey = `${x},${y}`;
    if (
      !isValidPosition(grid, position) ||
      visited.has(posKey) ||
      depth > maxDepth
    ) {
      continue;
    }
    
    // Mark as visited
    visited.add(posKey);
    
    // Call the visit callback
    if (!(x === start.x && y === start.y) && !(x === goal.x && y === goal.y)) {
      visitCallback(position);
    }
    
    // Check if goal reached
    if (x === goal.x && y === goal.y) {
      return node;
    }
    
    // If we haven't reached the depth limit, explore neighbors
    if (depth < maxDepth) {
      // Try each direction
      for (let i = 0; i < 4; i++) {
        const newPosition = {
          x: x + dx[i],
          y: y + dy[i],
        };
        
        // Add to stack if valid
        if (isValidPosition(grid, newPosition) && !visited.has(`${newPosition.x},${newPosition.y}`)) {
          stack.push({
            position: newPosition,
            parent: node,
            depth: depth + 1,
          });
        }
      }
    }
  }
  
  // No path found within the depth limit
  return null;
};

// Iterative Deepening Depth-First Search (IDDFS)
export const iddfs = async (
  grid: CellType[][],
  start: Position,
  goal: Position,
  visitCallback: (position: Position) => void,
  delay: number,
  isPausedRef: React.RefObject<boolean>,
  stopRef: React.RefObject<boolean>
): Promise<Node | null> => {
  // Define maximum depth as the grid size (which is the maximum possible path length)
  const maxPossibleDepth = grid.length * grid[0].length;
  
  // Iterate through increasing depth limits
  for (let depth = 0; depth <= maxPossibleDepth; depth++) {
    // Sleep between iterations to visualize the increasing depth
    await new Promise(resolve => setTimeout(resolve, delay));
    
    // Check if search should stop
    if (stopRef.current) {
      return null;
    }
    
    // Wait if paused
    while (isPausedRef.current && !stopRef.current) {
      await new Promise(resolve => setTimeout(resolve, 100));
    }
    
    // Run DLS with current depth limit
    const result = depthLimitedSearch(grid, start, goal, depth, visitCallback);
    
    // If path found, return it
    if (result) {
      return result;
    }
  }
  
  return null;
};

// Reconstruct path from goal to start
export const reconstructPath = (goalNode: Node): Position[] => {
  const path: Position[] = [];
  let current: Node | null = goalNode;
  
  while (current) {
    path.push(current.position);
    current = current.parent;
  }
  
  // Reverse to get start-to-goal path
  return path.reverse();
};
