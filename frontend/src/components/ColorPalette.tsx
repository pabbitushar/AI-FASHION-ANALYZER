import React from 'react';
import { motion } from 'framer-motion';
import { PaletteColor } from '../types';

interface ColorPaletteProps {
  palette: PaletteColor[];
}

export const ColorPalette: React.FC<ColorPaletteProps> = ({ palette }) => {
  if (!palette || palette.length === 0) return null;

  return (
    <div className="w-full">
      <h3 className="text-xl font-bold text-[var(--color-primary)] mb-6">Color Palette</h3>
      
      <div className="flex flex-wrap gap-4 md:gap-6">
        {palette.map((color, index) => (
          <motion.div 
            key={`${color.hex}-${index}`}
            initial={{ scale: 0, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            transition={{ delay: 0.2 + index * 0.1, type: 'spring' }}
            className="flex flex-col items-center gap-2 relative group"
          >
            <div 
              className={`w-14 h-14 md:w-16 md:h-16 rounded-full shadow-md border-2 border-white flex items-center justify-center transition-transform group-hover:scale-110 ${color.is_dominant ? 'ring-2 ring-[var(--color-accent)] ring-offset-2' : ''}`}
              style={{ backgroundColor: color.hex }}
            >
              {color.is_dominant && (
                <span className="absolute -top-2 bg-[var(--color-primary)] text-white text-[9px] font-bold px-1.5 py-0.5 rounded-full uppercase tracking-wider">
                  Main
                </span>
              )}
            </div>
            <div className="flex flex-col items-center">
              <span className="text-xs font-bold text-gray-800 uppercase tracking-wide">{color.name}</span>
              <span className="text-[10px] text-gray-500 font-medium">{Math.round(color.percentage)}%</span>
            </div>
          </motion.div>
        ))}
      </div>
      
      {/* Distribution Bar */}
      <div className="w-full h-3 rounded-full overflow-hidden mt-6 flex shadow-inner border border-gray-100">
        {palette.map((color, index) => (
          <motion.div
            key={`bar-${color.hex}-${index}`}
            initial={{ width: 0 }}
            animate={{ width: `${color.percentage}%` }}
            transition={{ duration: 1, delay: 0.5, ease: 'easeOut' }}
            className="h-full"
            style={{ backgroundColor: color.hex }}
            title={`${color.name} (${Math.round(color.percentage)}%)`}
          />
        ))}
      </div>
    </div>
  );
};
