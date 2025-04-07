
import React from 'react';
import { cn } from '@/lib/utils';

export type CellType = 'empty' | 'wall' | 'start' | 'goal' | 'visited' | 'path' | 'exploring';

interface GridCellProps {
  x: number;
  y: number;
  type: CellType;
  onClick: (x: number, y: number) => void;
}

const GridCell: React.FC<GridCellProps> = ({ x, y, type, onClick }) => {
  const getCellClassName = () => {
    switch (type) {
      case 'start':
        return 'bg-pathfinder-start';
      case 'goal':
        return 'bg-pathfinder-goal';
      case 'wall':
        return 'bg-pathfinder-wall';
      case 'visited':
        return 'bg-pathfinder-visited';
      case 'path':
        return 'bg-pathfinder-path';
      case 'exploring':
        return 'bg-pathfinder-exploring animate-pulse-light';
      default:
        return 'bg-pathfinder-grid';
    }
  };

  return (
    <div
      className={cn(
        'border border-gray-300 w-6 h-6 md:w-8 md:h-8 cursor-pointer transition-colors duration-200',
        getCellClassName()
      )}
      onClick={() => onClick(x, y)}
      data-testid={`cell-${x}-${y}`}
    />
  );
};

export default GridCell;
