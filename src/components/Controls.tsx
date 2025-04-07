
import React from 'react';
import { Button } from '@/components/ui/button';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Slider } from '@/components/ui/slider';

export type ToolType = 'start' | 'goal' | 'wall' | 'eraser';

interface ControlsProps {
  toolSelected: ToolType;
  setToolSelected: (tool: ToolType) => void;
  speed: number;
  setSpeed: (speed: number) => void;
  gridSize: number;
  setGridSize: (size: number) => void;
  onStart: () => void;
  onPause: () => void;
  onReset: () => void;
  isRunning: boolean;
  isPaused: boolean;
}

const Controls: React.FC<ControlsProps> = ({
  toolSelected,
  setToolSelected,
  speed,
  setSpeed,
  gridSize,
  setGridSize,
  onStart,
  onPause,
  onReset,
  isRunning,
  isPaused,
}) => {
  return (
    <div className="flex flex-col md:flex-row gap-4 p-4 bg-white rounded-lg shadow w-full max-w-4xl mb-6">
      <div className="flex-1 space-y-2">
        <label className="text-sm font-medium">Tool</label>
        <Select
          value={toolSelected}
          onValueChange={(value) => setToolSelected(value as ToolType)}
          disabled={isRunning}
        >
          <SelectTrigger>
            <SelectValue placeholder="Select a tool" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="start">Start Point</SelectItem>
            <SelectItem value="goal">Goal Point</SelectItem>
            <SelectItem value="wall">Wall</SelectItem>
            <SelectItem value="eraser">Eraser</SelectItem>
          </SelectContent>
        </Select>
      </div>

      <div className="flex-1 space-y-2">
        <label className="text-sm font-medium">Grid Size</label>
        <Select
          value={gridSize.toString()}
          onValueChange={(value) => setGridSize(parseInt(value))}
          disabled={isRunning}
        >
          <SelectTrigger>
            <SelectValue placeholder="Grid Size" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="10">10x10</SelectItem>
            <SelectItem value="15">15x15</SelectItem>
            <SelectItem value="20">20x20</SelectItem>
            <SelectItem value="25">25x25</SelectItem>
          </SelectContent>
        </Select>
      </div>

      <div className="flex-1 space-y-2">
        <label className="text-sm font-medium">Speed: {speed}x</label>
        <Slider 
          value={[speed]} 
          min={1} 
          max={10} 
          step={1} 
          onValueChange={(value) => setSpeed(value[0])}
        />
      </div>

      <div className="flex-1 flex items-end gap-2">
        {!isRunning ? (
          <Button 
            onClick={onStart} 
            className="flex-1 bg-green-600 hover:bg-green-700"
          >
            Start
          </Button>
        ) : (
          <>
            {!isPaused ? (
              <Button 
                onClick={onPause} 
                className="flex-1 bg-amber-500 hover:bg-amber-600"
              >
                Pause
              </Button>
            ) : (
              <Button 
                onClick={onStart} 
                className="flex-1 bg-green-600 hover:bg-green-700"
              >
                Resume
              </Button>
            )}
          </>
        )}
        <Button 
          onClick={onReset} 
          variant="outline" 
          className="flex-1"
        >
          Reset
        </Button>
      </div>
    </div>
  );
};

export default Controls;
