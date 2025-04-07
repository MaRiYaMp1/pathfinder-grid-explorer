import React, { useState, useRef, useEffect, useCallback } from 'react';
import Grid from '@/components/Grid';
import Controls from '@/components/Controls';
import { ToolType } from '@/components/Controls';
import { CellType } from '@/components/GridCell';
import { Position, Node, iddfs, reconstructPath } from '@/lib/pathfinder';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { useToast } from '@/components/ui/use-toast';

const PathfinderApp: React.FC = () => {
  const { toast } = useToast();
  const [gridSize, setGridSize] = useState<number>(15);
  const [grid, setGrid] = useState<CellType[][]>([]);
  const [toolSelected, setToolSelected] = useState<ToolType>('wall');
  const [speed, setSpeed] = useState<number>(5);
  const [startPosition, setStartPosition] = useState<Position | null>(null);
  const [goalPosition, setGoalPosition] = useState<Position | null>(null);
  const [isRunning, setIsRunning] = useState(false);
  const [isPaused, setIsPaused] = useState(false);
  const [pathFound, setPathFound] = useState(false);
  const [exploredCells, setExploredCells] = useState(0);
  
  const isPausedRef = useRef(false);
  const stopRef = useRef(false);

  const initializeGrid = useCallback(() => {
    const newGrid: CellType[][] = Array(gridSize)
      .fill('empty')
      .map(() => Array(gridSize).fill('empty'));
    setGrid(newGrid);
    setStartPosition(null);
    setGoalPosition(null);
    setPathFound(false);
    setExploredCells(0);
  }, [gridSize]);

  const handleReset = () => {
    stopRef.current = true;
    setTimeout(() => {
      stopRef.current = false;
      setIsRunning(false);
      setIsPaused(false);
      initializeGrid();
    }, 100);
  };

  const generateRandomMaze = () => {
    const newGrid: CellType[][] = Array(gridSize)
      .fill('empty')
      .map(() => Array(gridSize).fill('empty'));
    
    for (let y = 0; y < gridSize; y++) {
      for (let x = 0; x < gridSize; x++) {
        if (Math.random() < 0.3) {
          newGrid[y][x] = 'wall';
        }
      }
    }
    
    setStartPosition(null);
    setGoalPosition(null);
    setGrid(newGrid);
    setPathFound(false);
    setExploredCells(0);
  };

  const handleCellClick = (x: number, y: number) => {
    if (isRunning) return;

    const newGrid = [...grid.map(row => [...row])];
    
    if (toolSelected === 'start') {
      if (startPosition) {
        newGrid[startPosition.y][startPosition.x] = 'empty';
      }
      newGrid[y][x] = 'start';
      setStartPosition({ x, y });
    } else if (toolSelected === 'goal') {
      if (goalPosition) {
        newGrid[goalPosition.y][goalPosition.x] = 'empty';
      }
      newGrid[y][x] = 'goal';
      setGoalPosition({ x, y });
    } else if (toolSelected === 'wall') {
      if (
        !(startPosition && startPosition.x === x && startPosition.y === y) &&
        !(goalPosition && goalPosition.x === x && goalPosition.y === y)
      ) {
        newGrid[y][x] = 'wall';
      }
    } else if (toolSelected === 'eraser') {
      if (startPosition && startPosition.x === x && startPosition.y === y) {
        setStartPosition(null);
      } else if (goalPosition && goalPosition.x === x && goalPosition.y === y) {
        setGoalPosition(null);
      }
      newGrid[y][x] = 'empty';
    }
    
    setGrid(newGrid);
  };

  const handleStart = async () => {
    if (!startPosition || !goalPosition) {
      toast({
        title: "Missing positions",
        description: "Please select both start and goal positions",
        variant: "destructive",
      });
      return;
    }
    
    if (isRunning && isPaused) {
      setIsPaused(false);
      isPausedRef.current = false;
      return;
    }
    
    setIsRunning(true);
    setIsPaused(false);
    isPausedRef.current = false;
    stopRef.current = false;
    setPathFound(false);
    
    const newGrid = [...grid.map(row => [...row])];
    for (let y = 0; y < gridSize; y++) {
      for (let x = 0; x < gridSize; x++) {
        if (newGrid[y][x] === 'visited' || newGrid[y][x] === 'path' || newGrid[y][x] === 'exploring') {
          newGrid[y][x] = 'empty';
        }
      }
    }
    
    if (startPosition) newGrid[startPosition.y][startPosition.x] = 'start';
    if (goalPosition) newGrid[goalPosition.y][goalPosition.x] = 'goal';
    
    setGrid(newGrid);
    setExploredCells(0);
    
    const markCellAsVisited = (position: Position) => {
      if (isRunning) {
        const { x, y } = position;
        
        setGrid(prevGrid => {
          const newGrid = [...prevGrid.map(row => [...row])];
          if (
            !(startPosition && x === startPosition.x && y === startPosition.y) &&
            !(goalPosition && x === goalPosition.x && y === goalPosition.y)
          ) {
            newGrid[y][x] = 'exploring';
            setTimeout(() => {
              setGrid(prevGrid => {
                const newestGrid = [...prevGrid.map(row => [...row])];
                if (
                  !(startPosition && x === startPosition.x && y === startPosition.y) &&
                  !(goalPosition && x === goalPosition.x && y === goalPosition.y) &&
                  newestGrid[y][x] === 'exploring'
                ) {
                  newestGrid[y][x] = 'visited';
                }
                return newestGrid;
              });
            }, 1000 / speed);
          }
          return newGrid;
        });
        
        setExploredCells(prev => prev + 1);
      }
    };
    
    const result = await iddfs(
      grid,
      startPosition,
      goalPosition,
      markCellAsVisited,
      1000 / (speed * 2),
      isPausedRef,
      stopRef
    );
    
    if (result && !stopRef.current) {
      const path = reconstructPath(result);
      
      for (let i = 1; i < path.length - 1; i++) {
        if (stopRef.current) break;
        
        const { x, y } = path[i];
        await new Promise(resolve => setTimeout(resolve, 100 / speed));
        
        setGrid(prevGrid => {
          const newGrid = [...prevGrid.map(row => [...row])];
          newGrid[y][x] = 'path';
          return newGrid;
        });
      }
      
      setPathFound(true);
      toast({
        title: "Path found!",
        description: `Path length: ${path.length - 1} steps`,
      });
    } else if (!stopRef.current) {
      toast({
        title: "No path found",
        description: "There is no valid path between start and goal",
        variant: "destructive",
      });
    }
    
    setIsRunning(false);
  };

  const handlePause = () => {
    setIsPaused(true);
    isPausedRef.current = true;
  };

  useEffect(() => {
    initializeGrid();
  }, [gridSize, initializeGrid]);

  useEffect(() => {
    initializeGrid();
  }, [initializeGrid]);

  return (
    <div className="min-h-screen bg-gray-100 flex flex-col items-center py-8 px-4">
      <h1 className="text-3xl font-bold mb-2">Pathfinder Grid Explorer</h1>
      <p className="text-gray-600 mb-6 text-center">
        Visualize how the Iterative Deepening Depth-First Search (IDDFS) algorithm finds the shortest path
      </p>

      <div className="w-full max-w-4xl">
        <Controls
          toolSelected={toolSelected}
          setToolSelected={setToolSelected}
          speed={speed}
          setSpeed={setSpeed}
          gridSize={gridSize}
          setGridSize={setGridSize}
          onStart={handleStart}
          onPause={handlePause}
          onReset={handleReset}
          isRunning={isRunning}
          isPaused={isPaused}
        />

        <div className="bg-white p-6 rounded-lg shadow-md mb-6">
          <div className="flex flex-col md:flex-row gap-4 items-start">
            <div className="flex-1 flex flex-col items-center">
              <div className="relative overflow-auto p-2 border border-gray-200 rounded-lg">
                <Grid grid={grid} onCellClick={handleCellClick} />
              </div>
            </div>

            <div className="flex-1 flex flex-col space-y-4">
              <Card className="p-4">
                <h3 className="font-bold mb-2">Legend</h3>
                <div className="grid grid-cols-2 gap-2">
                  <div className="flex items-center">
                    <div className="w-4 h-4 bg-pathfinder-start mr-2" />
                    <span>Start</span>
                  </div>
                  <div className="flex items-center">
                    <div className="w-4 h-4 bg-pathfinder-goal mr-2" />
                    <span>Goal</span>
                  </div>
                  <div className="flex items-center">
                    <div className="w-4 h-4 bg-pathfinder-wall mr-2" />
                    <span>Wall</span>
                  </div>
                  <div className="flex items-center">
                    <div className="w-4 h-4 bg-pathfinder-visited mr-2" />
                    <span>Visited</span>
                  </div>
                  <div className="flex items-center">
                    <div className="w-4 h-4 bg-pathfinder-path mr-2" />
                    <span>Path</span>
                  </div>
                  <div className="flex items-center">
                    <div className="w-4 h-4 bg-pathfinder-exploring animate-pulse-light mr-2" />
                    <span>Exploring</span>
                  </div>
                </div>
              </Card>

              <Card className="p-4">
                <h3 className="font-bold mb-2">Status</h3>
                <div className="space-y-2">
                  <div>
                    <strong>Algorithm:</strong> IDDFS
                  </div>
                  <div>
                    <strong>Explored cells:</strong> {exploredCells}
                  </div>
                  <div>
                    <strong>Status:</strong>{" "}
                    {isRunning
                      ? isPaused
                        ? "Paused"
                        : "Running"
                      : pathFound
                      ? "Path Found"
                      : "Ready"}
                  </div>
                </div>
              </Card>
              
              <Button 
                onClick={generateRandomMaze} 
                disabled={isRunning} 
                className="w-full"
              >
                Generate Random Maze
              </Button>
              
              {!startPosition && !isRunning && (
                <Alert>
                  <AlertDescription>
                    Select the <strong>Start Point</strong> tool and click on the grid to place the starting position.
                  </AlertDescription>
                </Alert>
              )}
              
              {!goalPosition && startPosition && !isRunning && (
                <Alert>
                  <AlertDescription>
                    Select the <strong>Goal Point</strong> tool and click on the grid to place the goal position.
                  </AlertDescription>
                </Alert>
              )}
              
              {startPosition && goalPosition && !isRunning && !pathFound && (
                <Alert>
                  <AlertDescription>
                    Click <strong>Start</strong> to begin pathfinding, or add walls using the Wall tool.
                  </AlertDescription>
                </Alert>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PathfinderApp;
