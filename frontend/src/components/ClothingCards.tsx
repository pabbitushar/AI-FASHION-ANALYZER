import React from 'react';
import { motion } from 'framer-motion';
import { ClothingItem } from '../types';

interface ClothingCardsProps {
  items: ClothingItem[];
  itemCount: number;
}

export const ClothingCards: React.FC<ClothingCardsProps> = ({ items, itemCount }) => {
  if (!items || items.length === 0) return null;

  return (
    <div className="w-full">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-xl font-bold text-[var(--color-primary)]">What we found</h3>
        <span className="bg-gray-100 text-gray-600 text-xs font-semibold px-3 py-1 rounded-full">
          {itemCount} {itemCount === 1 ? 'piece' : 'pieces'} detected
        </span>
      </div>
      
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        {items.map((item, index) => (
          <motion.div
            key={`${item.display_name}-${index}`}
            whileHover={{ y: -2, boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)' }}
            className="bg-white border border-gray-100 rounded-2xl p-4 flex gap-4 items-center shadow-sm transition-all"
          >
            <div className="w-12 h-12 bg-gray-50 rounded-xl flex items-center justify-center text-2xl shrink-0">
              {item.icon}
            </div>
            
            <div className="flex flex-col flex-1 min-w-0">
              <h4 className="font-bold text-gray-900 truncate">{item.display_name}</h4>
              <p className="text-xs text-gray-500 capitalize">{item.category}</p>
              
              <div className="flex items-center gap-2 mt-2">
                <div 
                  className="w-3 h-3 rounded-full border border-gray-200 shadow-sm"
                  style={{ backgroundColor: item.color_hex }}
                />
                <span className="text-xs font-medium text-gray-600 capitalize">{item.color}</span>
              </div>
            </div>
            
            <div className="flex flex-col items-end justify-between h-full py-1">
              <span className="text-[10px] font-bold text-gray-400 bg-gray-50 px-2 py-0.5 rounded">
                {Math.round(item.confidence * 100)}%
              </span>
            </div>
          </motion.div>
        ))}
      </div>
    </div>
  );
};
