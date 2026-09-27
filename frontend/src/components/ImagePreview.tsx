

import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { ClothingItem } from '../types';

interface ImagePreviewProps {
  imageUrl: string;
  items: ClothingItem[];
}

export const ImagePreview: React.FC<ImagePreviewProps> = ({ imageUrl, items }) => {
  const [imageLoaded, setImageLoaded] = useState(false);

  // We only want to animate boxes after the image is fully loaded to ensure correct positioning
  return (
    <div className="w-full bg-gray-100 rounded-3xl overflow-hidden shadow-sm border border-gray-200 relative aspect-[3/4] md:aspect-auto md:min-h-[600px] flex items-center justify-center">
      
      {/* Skeleton loader for image */}
      {!imageLoaded && (
        <div className="absolute inset-0 animate-pulse bg-gray-200" />
      )}

      <div className="relative w-full h-full flex items-center justify-center">
        <img
          src={imageUrl}
          alt="Analyzed outfit"
          className="w-full h-full object-contain"
          onLoad={() => setImageLoaded(true)}
          style={{ opacity: imageLoaded ? 1 : 0, transition: 'opacity 0.3s ease-in-out' }}
        />
        
        {/* Bounding Boxes */}
        {imageLoaded && items.map((item, index) => {
          if (!item.bbox || item.bbox.length !== 4) return null;
          
          const [x1, y1, x2, y2] = item.bbox;
          const left = `${x1 * 100}%`;
          const top = `${y1 * 100}%`;
          const width = `${(x2 - x1) * 100}%`;
          const height = `${(y2 - y1) * 100}%`;

          return (
            <motion.div
              key={`${item.display_name}-${index}`}
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: 0.5 + index * 0.15, duration: 0.4 }}
              className="absolute border-2 border-white/80 shadow-[0_0_0_1px_rgba(0,0,0,0.1),inset_0_0_0_1px_rgba(0,0,0,0.1)] pointer-events-none rounded-sm"
              style={{
                left,
                top,
                width,
                height,
                borderColor: item.color_hex || 'white'
              }}
            >
              <div 
                className="absolute -top-3 -left-0.5 transform -translate-y-full bg-black text-white text-xs font-bold px-2 py-1 rounded shadow-md flex items-center gap-1 whitespace-nowrap"
              >
                <span>{item.icon}</span>
                <span>{item.display_name}</span>
              </div>
            </motion.div>
          );
        })}
      </div>
    </div>
  );
};
