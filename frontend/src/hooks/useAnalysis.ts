import { useState } from 'react';
import { AppView, AnalysisResult } from '../types';
import { analyzeOutfit, getConfig } from '../services/api';

export const useAnalysis = () => {
  const [view, setView] = useState<AppView>('landing');
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [preview, setPreview] = useState<string | null>(null);
  const [result, setResult] = useState<AnalysisResult | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isDemo, setIsDemo] = useState(false);

  const selectFile = (file: File) => {
    // Simple client-side validation
    if (!['image/jpeg', 'image/png', 'image/webp'].includes(file.type)) {
      setError('Invalid file type. Please upload a JPG, PNG, or WebP image.');
      return;
    }
    if (file.size > 10 * 1024 * 1024) {
      setError('File is too large. Please upload an image under 10MB.');
      return;
    }
    
    setError(null);
    setSelectedFile(file);
    setPreview(URL.createObjectURL(file));
  };

  const startAnalysis = async () => {
    if (!selectedFile) return;
    
    setView('analyzing');
    setError(null);
    
    try {
      const config = await getConfig().catch(() => ({ demo_mode: false }));
      setIsDemo(config.demo_mode);
      
      const response = await analyzeOutfit(selectedFile);
      
      if (response.success && response.data) {
        setResult(response.data);
        setView('results');
      } else {
        throw new Error(response.error || response.message || 'Failed to analyze outfit');
      }
    } catch (err: any) {
      setError(err.message || 'An unexpected error occurred. Please try again.');
      setView('error');
    }
  };

  const reset = () => {
    setSelectedFile(null);
    setPreview(null);
    setResult(null);
    setError(null);
    setView('upload'); // Go to upload on reset
  };

  const goToUpload = () => {
    setView('upload');
  };

  return {
    view,
    selectedFile,
    preview,
    result,
    error,
    isDemo,
    selectFile,
    startAnalysis,
    reset,
    goToUpload,
  };
};
