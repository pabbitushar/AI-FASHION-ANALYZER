import React, { useRef, useState } from 'react';
import { motion } from 'framer-motion';
import { Upload as UploadIcon, Image as ImageIcon } from 'lucide-react';

interface UploadProps {
  onFileSelect: (file: File) => void;
  selectedFile: File | null;
  previewUrl: string | null;
  onAnalyze: () => void;
  error?: string | null;
}

export const Upload: React.FC<UploadProps> = ({ 
  onFileSelect, 
  selectedFile, 
  previewUrl, 
  onAnalyze,
  error 
}) => {
  const [isDragging, setIsDragging] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
    
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      onFileSelect(e.dataTransfer.files[0]);
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      onFileSelect(e.target.files[0]);
    }
  };

  return (
    <motion.div
      key="upload"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -20 }}
      className="w-full max-w-2xl mx-auto flex flex-col mt-12"
    >
      <div className="text-center mb-8">
        <h2 className="text-3xl font-bold mb-2">Upload your photo</h2>
        <p className="text-[var(--color-secondary)]">For best results, use a full-body shot with good lighting.</p>
      </div>

      {!selectedFile ? (
        <div
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
          className={`
            border-3 border-dashed rounded-3xl min-h-[350px] flex flex-col items-center justify-center p-8 transition-colors
            ${isDragging ? 'border-[var(--color-accent)] bg-gray-50' : 'border-gray-200 hover:border-gray-300'}
          `}
        >
          <div className="w-16 h-16 bg-gray-50 rounded-full flex items-center justify-center mb-4 text-gray-400">
            <UploadIcon size={32} />
          </div>
          
          <p className="text-xl font-bold mb-1">Drop your outfit photo here</p>
          <p className="text-gray-500 mb-6">
            or{' '}
            <button 
              onClick={() => fileInputRef.current?.click()} 
              className="text-[var(--color-primary)] font-semibold underline underline-offset-4 decoration-2 decoration-gray-300 hover:decoration-[var(--color-primary)] transition-colors"
            >
              Choose a photo
            </button>
          </p>
          
          <p className="text-xs text-gray-400 font-medium">JPG, PNG, or WebP up to 10MB</p>
          
          <input
            type="file"
            ref={fileInputRef}
            onChange={handleChange}
            accept="image/jpeg, image/png, image/webp"
            className="hidden"
          />
        </div>
      ) : (
        <motion.div 
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          className="bg-white p-4 rounded-3xl shadow-sm border border-gray-100 flex flex-col gap-6"
        >
          <div className="relative rounded-2xl overflow-hidden bg-gray-100 flex items-center justify-center min-h-[400px] max-h-[600px]">
            {previewUrl && (
              <img 
                src={previewUrl} 
                alt="Selected outfit" 
                className="w-full h-full object-contain"
              />
            )}
          </div>
          
          <div className="flex flex-col sm:flex-row items-center justify-between gap-4 px-2">
            <div className="flex items-center gap-3">
              <div className="p-2 bg-gray-100 rounded-lg">
                <ImageIcon size={20} className="text-gray-600" />
              </div>
              <div className="flex flex-col">
                <span className="text-sm font-semibold truncate max-w-[150px] sm:max-w-[200px]">
                  {selectedFile.name}
                </span>
                <span className="text-xs text-gray-500">
                  {(selectedFile.size / (1024 * 1024)).toFixed(2)} MB
                </span>
              </div>
            </div>
            
            <div className="flex items-center gap-3 w-full sm:w-auto">
              <button
                onClick={() => fileInputRef.current?.click()}
                className="text-sm font-medium text-gray-500 hover:text-gray-800 transition-colors px-4 py-2"
              >
                Change
              </button>
              <button
                onClick={onAnalyze}
                className="flex-1 sm:flex-none bg-[var(--color-accent)] text-white px-8 py-3 rounded-full font-semibold hover:bg-black transition-all hover:scale-[1.02] active:scale-[0.98]"
              >
                Analyze outfit →
              </button>
            </div>
          </div>
          <input
            type="file"
            ref={fileInputRef}
            onChange={handleChange}
            accept="image/jpeg, image/png, image/webp"
            className="hidden"
          />
        </motion.div>
      )}

      {error && (
        <motion.p 
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-red-500 text-sm font-medium text-center mt-4 bg-red-50 py-2 px-4 rounded-lg"
        >
          {error}
        </motion.p>
      )}

      <p className="text-center text-xs text-gray-400 mt-8 italic">
        Your photo is processed for this analysis and isn't intended to be stored.
      </p>
    </motion.div>
  );
};
