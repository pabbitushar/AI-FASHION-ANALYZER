from abc import ABC, abstractmethod

class FashionAnalyzer(ABC):
    @abstractmethod
    def analyze(self, image) -> dict:
        """Analyze an image and return structured fashion data."""
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """Check if this analyzer is ready."""
        pass
