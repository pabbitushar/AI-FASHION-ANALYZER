import random
from models.schemas import AnalysisResult, ClothingItem, PaletteColor, StyleClassification
from ml.base import FashionAnalyzer

class DemoAnalyzer(FashionAnalyzer):
    def is_available(self) -> bool:
        return True

    def analyze(self, image) -> dict:
        presets = [
            {
                "items": [
                    ClothingItem(category="t-shirt", display_name="T-Shirt", color="black", color_hex="#1a1a1a", confidence=0.95, bbox=[0.2, 0.1, 0.8, 0.5], icon="👕"),
                    ClothingItem(category="jeans", display_name="Jeans", color="blue", color_hex="#2a52be", confidence=0.92, bbox=[0.2, 0.5, 0.8, 0.9], icon="👖")
                ],
                "palette": [
                    PaletteColor(name="black", hex="#1a1a1a", percentage=55.0, is_dominant=True),
                    PaletteColor(name="blue", hex="#2a52be", percentage=45.0, is_dominant=False)
                ],
                "style": StyleClassification(label="casual", secondary_label="everyday", confidence=0.88, insight="A classic, effortless everyday look combining basic staples.")
            },
            {
                "items": [
                    ClothingItem(category="blazer", display_name="Blazer", color="navy", color_hex="#000080", confidence=0.98, bbox=[0.1, 0.1, 0.9, 0.6], icon="🧥"),
                    ClothingItem(category="trousers", display_name="Trousers", color="navy", color_hex="#000080", confidence=0.91, bbox=[0.2, 0.6, 0.8, 1.0], icon="👖")
                ],
                "palette": [
                    PaletteColor(name="navy", hex="#000080", percentage=80.0, is_dominant=True),
                    PaletteColor(name="white", hex="#ffffff", percentage=20.0, is_dominant=False)
                ],
                "style": StyleClassification(label="formal", secondary_label="business", confidence=0.94, insight="Sharp and professional monochromatic tailoring.")
            },
            {
                "items": [
                    ClothingItem(category="hoodie", display_name="Hoodie", color="gray", color_hex="#808080", confidence=0.89, bbox=[0.15, 0.1, 0.85, 0.55], icon="🧥"),
                    ClothingItem(category="sweatpants", display_name="Sweatpants", color="black", color_hex="#000000", confidence=0.85, bbox=[0.2, 0.55, 0.8, 0.95], icon="👖")
                ],
                "palette": [
                    PaletteColor(name="gray", hex="#808080", percentage=60.0, is_dominant=True),
                    PaletteColor(name="black", hex="#000000", percentage=40.0, is_dominant=False)
                ],
                "style": StyleClassification(label="sporty", secondary_label="athleisure", confidence=0.91, insight="Comfort-first athleisure perfect for on-the-go days.")
            },
            {
                "items": [
                    ClothingItem(category="jacket", display_name="Oversized Jacket", color="olive", color_hex="#808000", confidence=0.88, bbox=[0.1, 0.1, 0.9, 0.6], icon="🧥"),
                    ClothingItem(category="cargo", display_name="Cargo Pants", color="beige", color_hex="#f5f5dc", confidence=0.87, bbox=[0.15, 0.6, 0.85, 1.0], icon="👖")
                ],
                "palette": [
                    PaletteColor(name="olive", hex="#808000", percentage=50.0, is_dominant=True),
                    PaletteColor(name="beige", hex="#f5f5dc", percentage=50.0, is_dominant=False)
                ],
                "style": StyleClassification(label="streetwear", secondary_label="utilitarian", confidence=0.85, insight="A trendy streetwear fit with utilitarian elements.")
            },
            {
                "items": [
                    ClothingItem(category="shirt", display_name="Button-up", color="white", color_hex="#ffffff", confidence=0.93, bbox=[0.2, 0.1, 0.8, 0.5], icon="👔"),
                    ClothingItem(category="chinos", display_name="Chinos", color="tan", color_hex="#d2b48c", confidence=0.90, bbox=[0.2, 0.5, 0.8, 0.9], icon="👖")
                ],
                "palette": [
                    PaletteColor(name="white", hex="#ffffff", percentage=45.0, is_dominant=False),
                    PaletteColor(name="tan", hex="#d2b48c", percentage=55.0, is_dominant=True)
                ],
                "style": StyleClassification(label="smart casual", secondary_label="preppy", confidence=0.92, insight="A polished smart casual combination blending comfort and sophistication.")
            },
            {
                "items": [
                    ClothingItem(category="dress", display_name="Maxi Dress", color="floral", color_hex="#ffb6c1", confidence=0.96, bbox=[0.2, 0.1, 0.8, 0.9], icon="👗")
                ],
                "palette": [
                    PaletteColor(name="pink", hex="#ffb6c1", percentage=70.0, is_dominant=True),
                    PaletteColor(name="green", hex="#008000", percentage=30.0, is_dominant=False)
                ],
                "style": StyleClassification(label="boho", secondary_label="summer", confidence=0.89, insight="A breezy, free-spirited bohemian dress with floral accents.")
            }
        ]
        
        selected = random.choice(presets)
        
        result = AnalysisResult(
            items=selected["items"],
            palette=selected["palette"],
            style=selected["style"],
            item_count=len(selected["items"]),
            is_demo=True
        )
        return result.model_dump()
