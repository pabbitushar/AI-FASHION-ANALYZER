export interface ClothingItem {
  category: string;
  display_name: string;
  color: string;
  color_hex: string;
  confidence: number;
  bbox: number[];  // [x1, y1, x2, y2] normalized 0-1
  icon: string;
}

export interface PaletteColor {
  name: string;
  hex: string;
  percentage: number;
  is_dominant: boolean;
}

export interface StyleClassification {
  label: string;
  secondary_label: string | null;
  confidence: number;
  insight: string;
}

export interface AnalysisResult {
  items: ClothingItem[];
  palette: PaletteColor[];
  style: StyleClassification;
  item_count: number;
  is_demo: boolean;
}

export interface AnalysisResponse {
  success: boolean;
  data: AnalysisResult | null;
  error: string | null;
  message: string | null;
}

export type AppView = 'landing' | 'upload' | 'analyzing' | 'results' | 'error';
