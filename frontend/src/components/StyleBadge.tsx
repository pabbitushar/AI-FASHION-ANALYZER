import React from 'react';
import { StyleClassification } from '../types';
import { Tag } from 'lucide-react';

interface StyleBadgeProps {
  style: StyleClassification;
}

export const StyleBadge: React.FC<StyleBadgeProps> = ({ style }) => {
  if (!style) return null;

  return (
    <div className="w-full flex flex-col items-start gap-3">
      <div className="flex items-center gap-2 text-gray-500">
        <Tag size={16} />
        <span className="text-sm font-semibold uppercase tracking-wider">Style Direction</span>
      </div>
      
      <div className="flex flex-wrap items-end gap-3">
        <h2 className="text-3xl md:text-4xl font-black text-[var(--color-primary)] tracking-tight">
          {style.label}
        </h2>
        {style.secondary_label && (
          <span className="text-xl md:text-2xl font-bold text-gray-400 mb-0.5">
            / {style.secondary_label}
          </span>
        )}
      </div>
      
      <div className="flex items-center gap-2 mt-1">
        <div className="h-1.5 w-24 bg-gray-200 rounded-full overflow-hidden">
          <div 
            className="h-full bg-[var(--color-accent)] rounded-full"
            style={{ width: `${style.confidence * 100}%` }}
          />
        </div>
        <span className="text-xs font-semibold text-gray-500">
          {Math.round(style.confidence * 100)}% match
        </span>
      </div>
    </div>
  );
};
