"""
Base translation provider module

Provides abstract base class for translation providers.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional


class TranslationProvider(ABC):
    """Abstract base class for translation providers"""
    
    @property
    @abstractmethod
    def name(self) -> str:
        """
        Get provider name
        
        Returns:
            str: Provider name
        """
        pass
    
    @abstractmethod
    def translate(self, content: str, languages: List[str], **kwargs) -> str:
        """
        Execute translation
        
        Args:
            content: Content to translate
            languages: Target language list
            **kwargs: Additional parameters
            
        Returns:
            str: Translated content
        """
        pass
    
    @abstractmethod
    def validate_credentials(self) -> bool:
        """
        Validate if credentials are valid
        
        Returns:
            bool: Whether credentials are valid
        """
        pass
    
    def get_language_name(self, lang_code: str) -> str:
        """
        Get language name corresponding to language code
        
        Args:
            lang_code: Language code
            
        Returns:
            str: Language name
        """
        language_map = {
            "zh-Hans": "中文",
            "zh-Hant": "繁體中文",
            "en": "English", 
            "ja": "日本語",
            "ko": "한국어",
            "fr": "Français",
            "de": "Deutsch",
            "es": "Español",
            "it": "Italiano",
            "pt": "Português",
            "pt-PT": "Português (Portugal)",
            "ru": "Русский",
            "vi": "Tiếng Việt",
            "th": "ไทย",
            "hi": "हिन्दी",
            "ar": "العربية",
            "tr": "Türkçe",
            "pl": "Polski",
            "nl": "Nederlands",
            "sv": "Svenska",
            "da": "Dansk",
            "no": "Norsk",
            "nb": "Norsk Bokmål",
            "fi": "Suomi",
            "cs": "Čeština",
            "sk": "Slovenčina",
            "hu": "Magyar",
            "ro": "Română",
            "bg": "български",
            "hr": "Hrvatski",
            "sl": "Slovenščina",
            "et": "Eesti",
            "lv": "Latviešu",
            "lt": "Lietuvių",
            "mt": "Malti",
            "el": "Ελληνικά",
            "ca": "Català",
            "eu": "Euskara",
            "gl": "Galego",
            "af": "Afrikaans",
            "zu": "IsiZulu",
            "xh": "isiXhosa",
            "st": "Sesotho",
            "sw": "Kiswahili",
            "yo": "Èdè Yorùbá",
            "ig": "Asụsụ Igbo",
            "ha": "Hausa",
            "am": "አማርኛ",
            "or": "ଓଡ଼ିଆ",
            "bn": "বাংলা",
            "gu": "ગુજરાતી",
            "pa": "ਪੰਜਾਬੀ",
            "te": "తెలుగు",
            "kn": "ಕನ್ನಡ",
            "ml": "മലയാളം",
            "ta": "தமிழ்",
            "si": "සිංහල",
            "my": "မြန်မာဘာသာ",
            "km": "ភាសាខ្មែរ",
            "lo": "ລາວ",
            "ne": "नेपाली",
            "ur": "اردو",
            "fa": "فارسی",
            "ps": "پښتو",
            "sd": "سنڌي",
            "he": "עברית",
            "yue": "粵語"
        }
        return language_map.get(lang_code, lang_code)
    
    def build_translation_prompt(self, content: str, languages: List[str], mode: str = "gen") -> str:
        """
        Build translation prompt
        
        Args:
            content: Content to translate
            languages: Target language list
            mode: Translation mode ("gen" or "trans")
            
        Returns:
            str: Translation prompt
        """
        language_names = [self.get_language_name(lang) for lang in languages]
        languages_str = "、".join(language_names)
        
        # Build JSON keys example
        json_keys = ", ".join([f'"{lang}": "..."' for lang in languages])
        
        if mode == "trans":
            prompt = f"""Translate the following README content into these languages: {languages_str}

Original content:
{content}

IMPORTANT: You MUST return the result as a valid JSON object with language codes as keys.
Each value should be the complete translated README content for that language.
Maintain the original Markdown format and structure in each translation.

Return ONLY a JSON object in this exact format (no other text):
```json
{{
  {json_keys}
}}
```

The JSON keys must be exactly: {', '.join(languages)}
Each value must contain the complete translated README in that language."""
        else:
            prompt = f"""Generate README documentation for the following project in these languages: {languages_str}

Project information:
{content}

IMPORTANT: You MUST return the result as a valid JSON object with language codes as keys.
Each value should be a complete README document for that language.
Include introduction, features, installation, and usage instructions.

Return ONLY a JSON object in this exact format (no other text):
```json
{{
  {json_keys}
}}
```

The JSON keys must be exactly: {', '.join(languages)}
Each value must contain a complete README document in that language."""
        
        return prompt
