import React from 'react';
import { AlertCircle, X } from 'lucide-react';

export const DemoBanner: React.FC = () => {
  const [visible, setVisible] = React.useState(true);

  if (!visible) return null;

  return (
    <div className="w-full bg-amber-50 border-b border-amber-200 py-2 px-4 relative z-50">
      <div className="max-w-7xl mx-auto flex items-center justify-center text-amber-800 text-sm font-medium gap-2">
        <AlertCircle size={16} />
        <p>Demo Mode — Results are simulated for demonstration purposes</p>
        <button 
          onClick={() => setVisible(false)}
          className="absolute right-4 text-amber-600 hover:text-amber-800 transition-colors"
          aria-label="Dismiss banner"
        >
          <X size={16} />
        </button>
      </div>
    </div>
  );
};
