"""Base translator interface."""
from abc import ABC, abstractmethod
from typing import Optional


class BaseTranslator(ABC):
    """Base class for translator implementations."""
    
    @abstractmethod
    def translate_text(self, text: str, target_lang: str) -> Optional[str]:
        """Translate text to target language.
        
        Args:
            text: Text to translate
            target_lang: Target language code
            
        Returns:
            Translated text or None if translation failed
        """
        pass 