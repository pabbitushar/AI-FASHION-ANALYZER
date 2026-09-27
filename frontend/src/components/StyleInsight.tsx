import React from 'react';
import { Quote } from 'lucide-react';

interface StyleInsightProps {
  insight: string;
}

export const StyleInsight: React.FC<StyleInsightProps> = ({ insight }) => {
  if (!insight) return null;

  return (
    <div className="relative p-6 bg-gray-50 rounded-2xl border-l-4 border-l-[var(--color-accent)] shadow-sm">
      <Quote className="absolute top-4 right-4 text-gray-200" size={32} />
      <h3 className="text-sm font-bold text-gray-400 uppercase tracking-widest mb-2">Insight</h3>
      <p className="text-lg text-gray-800 font-medium leading-relaxed italic relative z-10">
        "{insight}"
      </p>
    </div>
  );
};
