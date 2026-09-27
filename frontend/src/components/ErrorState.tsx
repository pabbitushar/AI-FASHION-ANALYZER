import React from 'react';
import { motion } from 'framer-motion';
import { AlertTriangle } from 'lucide-react';

interface ErrorStateProps {
  message: string;
  onRetry: () => void;
  onHome: () => void;
}

export const ErrorState: React.FC<ErrorStateProps> = ({ message, onRetry, onHome }) => {
  return (
    <motion.div
      key="error"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -20 }}
      className="flex flex-col items-center justify-center h-[60vh] max-w-md text-center"
    >
      <div className="w-20 h-20 bg-red-50 text-red-500 rounded-full flex items-center justify-center mb-6">
        <AlertTriangle size={32} />
      </div>
      
      <h2 className="text-2xl font-bold mb-3 text-[var(--color-primary)]">
        Analysis Failed
      </h2>
      
      <p className="text-[var(--color-secondary)] mb-8">
        {message}
      </p>
      
      <div className="flex flex-col gap-3 w-full">
        <button
          onClick={onRetry}
          className="w-full py-4 px-6 bg-[var(--color-accent)] text-white font-medium rounded-full hover:bg-black transition-transform hover:scale-[1.02] active:scale-[0.98]"
        >
          Try another photo
        </button>
        <button
          onClick={onHome}
          className="w-full py-4 px-6 text-[var(--color-secondary)] hover:text-[var(--color-primary)] font-medium transition-colors"
        >
          Back to home
        </button>
      </div>
    </motion.div>
  );
};
