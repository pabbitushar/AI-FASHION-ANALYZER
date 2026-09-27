import axios from 'axios';
import { AnalysisResponse } from '../types';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_URL,
});

export const analyzeOutfit = async (file: File): Promise<AnalysisResponse> => {
  const formData = new FormData();
  formData.append('file', file);
  
  const response = await api.post<AnalysisResponse>('/api/analyze', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  return response.data;
};

export const getHealth = async (): Promise<{ status: string; demo_mode: boolean }> => {
  const response = await api.get('/api/health');
  return response.data;
};

export const getConfig = async (): Promise<{ demo_mode: boolean; max_size: number; allowed_formats: string[] }> => {
  const response = await api.get('/api/config');
  return response.data;
};
