import React from 'react';
import { motion } from 'framer-motion';
import { AnalysisResult } from '../types';
import { ImagePreview } from './ImagePreview';
import { ClothingCards } from './ClothingCards';
import { ColorPalette } from './ColorPalette';
import { StyleBadge } from './StyleBadge';
import { StyleInsight } from './StyleInsight';
import { RefreshCw } from 'lucide-react';

interface ResultsProps {
  result: AnalysisResult;
  imageUrl: string;
  onReset: () => void;
}

const containerVariants = {
  hidden: { opacity: 0 },
  show: {
    opacity: 1,
    transition: { staggerChildren: 0.15 }
  }
};

const itemVariants = {
  hidden: { opacity: 0, y: 20 },
  show: { opacity: 1, y: 0, transition: { type: 'spring', stiffness: 300, damping: 24 } }
};

export const Results: React.FC<ResultsProps> = ({ result, imageUrl, onReset }) => {
  return (
    <motion.div
      key="results"
      variants={containerVariants}
      initial="hidden"
      animate="show"
      exit={{ opacity: 0, y: -20 }}
      className="w-full flex flex-col gap-10 mt-6"
    >
      <div className="flex flex-col lg:grid lg:grid-cols-2 gap-10 lg:gap-16 items-start">
        
        {/* Left Column: Image with Bboxes */}
        <motion.div variants={itemVariants} className="w-full sticky top-8">
          <ImagePreview 
            imageUrl={imageUrl} 
            items={result.items} 
          />
        </motion.div>
        
        {/* Right Column: Analysis */}
        <motion.div variants={itemVariants} className="w-full flex flex-col gap-12">
          
          <motion.div variants={itemVariants}>
            <StyleBadge style={result.style} />
          </motion.div>

          <motion.div variants={itemVariants}>
            <StyleInsight insight={result.style.insight} />
          </motion.div>
          
          <motion.div variants={itemVariants}>
            <ClothingCards items={result.items} itemCount={result.item_count} />
          </motion.div>

          {result.palette && result.palette.length > 0 && (
            <motion.div variants={itemVariants}>
              <ColorPalette palette={result.palette} />
            </motion.div>
          )}

          <motion.div variants={itemVariants} className="pt-8 pb-4">
            <button
              onClick={onReset}
              className="flex items-center justify-center gap-2 w-full py-4 bg-gray-100 text-[var(--color-primary)] font-semibold rounded-2xl hover:bg-gray-200 transition-colors"
            >
              <RefreshCw size={18} />
              Analyze another outfit
            </button>
          </motion.div>
          
        </motion.div>
      </div>
    </motion.div>
  );
};
