
import React from 'react';
import GridCell, { CellType } from './GridCell';

interface GridProps {
  grid: CellType[][];
  onCellClick: (x: number, y: number) => void;
}

const Grid: React.FC<GridProps> = ({ grid, onCellClick }) => {
  return (
    <div className="flex flex-col items-center">
      {grid.map((row, y) => (
        <div key={y} className="flex flex-row">
          {row.map((cell, x) => (
            <GridCell
              key={`${x}-${y}`}
              x={x}
              y={y}
              type={cell}
              onClick={onCellClick}
            />
          ))}
        </div>
      ))}
    </div>
  );
};

export default Grid;
