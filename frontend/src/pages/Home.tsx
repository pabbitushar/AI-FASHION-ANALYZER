import React from 'react';
import { useAnalysis } from '../hooks/useAnalysis';
import { Layout } from '../components/Layout';
import { Landing } from '../components/Landing';
import { Upload } from '../components/Upload';
import { AnalysisLoader } from '../components/AnalysisLoader';
import { Results } from '../components/Results';
import { ErrorState } from '../components/ErrorState';

export const Home: React.FC = () => {
  const {
    view,
    selectedFile,
    preview,
    result,
    error,
    isDemo,
    selectFile,
    startAnalysis,
    reset,
    goToUpload
  } = useAnalysis();

  return (
    <Layout isDemo={isDemo}>
      {view === 'landing' && <Landing onStart={goToUpload} />}
      
      {view === 'upload' && (
        <Upload 
          onFileSelect={selectFile}
          selectedFile={selectedFile}
          previewUrl={preview}
          onAnalyze={startAnalysis}
          error={error}
        />
      )}
      
      {view === 'analyzing' && <AnalysisLoader />}
      
      {view === 'results' && result && preview && (
        <Results 
          result={result}
          imageUrl={preview}
          onReset={reset}
        />
      )}

      {view === 'error' && (
        <ErrorState 
          message={error || 'An unexpected error occurred'} 
          onRetry={goToUpload} 
          onHome={reset} 
        />
      )}
    </Layout>
  );
};
