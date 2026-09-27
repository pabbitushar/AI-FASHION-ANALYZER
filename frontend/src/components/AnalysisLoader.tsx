import React, { useEffect, useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';

const messages = [
  "Looking at your outfit...",
  "Detecting clothing...",
  "Identifying colors...",
  "Understanding your look...",
  "Almost there..."
];

export const AnalysisLoader: React.FC = () => {
  const [index, setIndex] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setIndex((prev) => (prev < messages.length - 1 ? prev + 1 : prev));
    }, 1500);
    return () => clearInterval(interval);
  }, []);

  return (
    <motion.div
      key="loader"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className="flex flex-col items-center justify-center min-h-[60vh] gap-8"
    >
      <div className="relative flex items-center justify-center">
        {/* Outer pulsating ring */}
        <motion.div 
          className="absolute w-32 h-32 rounded-full border-4 border-gray-100"
          animate={{ scale: [1, 1.2, 1], opacity: [0.3, 1, 0.3] }}
          transition={{ duration: 2, repeat: Infinity, ease: "easeInOut" }}
        />
        
        {/* Middle scanning ring */}
        <motion.div 
          className="absolute w-24 h-24 rounded-full border-2 border-[var(--color-accent)] border-t-transparent border-r-transparent"
          animate={{ rotate: 360 }}
          transition={{ duration: 1.5, repeat: Infinity, ease: "linear" }}
        />
        
        {/* Inner core */}
        <motion.div 
          className="w-16 h-16 rounded-full bg-[var(--color-accent)] shadow-lg"
          animate={{ scale: [0.9, 1.1, 0.9] }}
          transition={{ duration: 2, repeat: Infinity, ease: "easeInOut" }}
        />
      </div>

      <div className="h-8 relative overflow-hidden flex items-center justify-center w-full">
        <AnimatePresence mode="wait">
          <motion.p
            key={index}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
            transition={{ duration: 0.3 }}
            className="text-lg font-medium text-[var(--color-primary)] absolute text-center"
          >
            {messages[index]}
          </motion.p>
        </AnimatePresence>
      </div>
      
      {/* Progress dots */}
      <div className="flex gap-1.5 mt-2">
        {messages.map((_, i) => (
          <motion.div 
            key={i}
            className={`w-1.5 h-1.5 rounded-full ${i <= index ? 'bg-[var(--color-accent)]' : 'bg-gray-200'}`}
            animate={i === index ? { scale: [1, 1.5, 1], opacity: [1, 0.5, 1] } : {}}
            transition={i === index ? { duration: 1, repeat: Infinity } : {}}
          />
        ))}
      </div>
    </motion.div>
  );
};
