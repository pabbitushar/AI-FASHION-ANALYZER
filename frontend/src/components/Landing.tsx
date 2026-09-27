import React, { useEffect, useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { ArrowRight, Sparkles } from 'lucide-react';

interface LandingProps {
  onStart: () => void;
}

export const Landing: React.FC<LandingProps> = ({ onStart }) => {
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  return (
    <motion.div
      key="landing"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className="flex flex-col items-center justify-center w-full min-h-[70vh]"
    >
      <div className="max-w-3xl w-full text-center flex flex-col items-center gap-6">
        
        {/* Animated Visualization */}
        <motion.div 
          className="relative w-48 h-64 mb-8"
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.8, delay: 0.2 }}
        >
          <div className="absolute inset-0 border-2 border-dashed border-gray-300 rounded-3xl overflow-hidden">
            <div className="absolute inset-x-0 bottom-0 h-1/2 bg-gradient-to-t from-gray-100 to-transparent opacity-50" />
            <motion.div 
              className="absolute w-full h-[2px] bg-[var(--color-accent)] shadow-[0_0_8px_rgba(0,0,0,0.3)]"
              animate={{ top: ['0%', '100%', '0%'] }}
              transition={{ duration: 4, repeat: Infinity, ease: 'linear' }}
            />
          </div>
          
          <AnimatePresence>
            {mounted && (
              <>
                <motion.div
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: 1 }}
                  className="absolute top-12 -left-12 bg-white px-3 py-1 rounded-full shadow-sm text-xs font-semibold flex items-center gap-1 border border-gray-100"
                >
                  <Sparkles size={12} className="text-amber-500" />
                  Top
                </motion.div>
                <motion.div
                  initial={{ opacity: 0, x: 20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: 1.5 }}
                  className="absolute bottom-16 -right-12 bg-white px-3 py-1 rounded-full shadow-sm text-xs font-semibold flex items-center gap-1 border border-gray-100"
                >
                  <Sparkles size={12} className="text-amber-500" />
                  Bottom
                </motion.div>
              </>
            )}
          </AnimatePresence>
        </motion.div>

        <motion.h1 
          className="text-5xl md:text-6xl font-bold tracking-tight text-[var(--color-primary)] leading-tight"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.3 }}
        >
          See what your <br className="hidden md:block" /> outfit says.
        </motion.h1>
        
        <motion.p 
          className="text-lg md:text-xl text-[var(--color-secondary)] max-w-xl mx-auto font-medium"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.4 }}
        >
          Upload a photo and let AI break down your look — the pieces, colors, and style direction hiding in your outfit.
        </motion.p>
        
        <motion.div
          className="mt-8 flex flex-col items-center gap-4"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.5 }}
        >
          <button
            onClick={onStart}
            className="flex items-center gap-2 bg-[var(--color-accent)] text-white px-8 py-4 rounded-full font-semibold text-lg hover:bg-black transition-all hover:scale-[1.03] active:scale-[0.97]"
          >
            Analyze My Outfit
            <ArrowRight size={20} />
          </button>
          <p className="text-sm text-gray-400 font-medium">No account required.</p>
        </motion.div>
      </div>
    </motion.div>
  );
};
