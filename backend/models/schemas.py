from pydantic import BaseModel
from typing import Optional

class ClothingItem(BaseModel):
    category: str
    display_name: str
    color: str
    color_hex: str
    confidence: float
    bbox: list[float]
    icon: str

class PaletteColor(BaseModel):
    name: str
    hex: str
    percentage: float
    is_dominant: bool

class StyleClassification(BaseModel):
    label: str
    secondary_label: Optional[str] = None
    confidence: float
    insight: str

class AnalysisResult(BaseModel):
    items: list[ClothingItem]
    palette: list[PaletteColor]
    style: StyleClassification
    item_count: int
    is_demo: bool

class AnalysisResponse(BaseModel):
    success: bool
    data: Optional[AnalysisResult] = None
    error: Optional[str] = None
    message: Optional[str] = None
