"""
Content parser module

Responsible for parsing multi-language README content from generation responses.
"""

import re
from typing import Dict, List, Optional
from ..models.types import ParsedReadme
from ..utils.json_extractor import extract_json_content
from ..utils.logger import debug, info, warning, error


class Parser:
    """Parser class, responsible for parsing multi-language README content"""
    
    def __init__(self):
        """Initialize parser"""
        # Only keep JSON format parsing, remove regex patterns
        self.language_patterns = {}
        
        # Special handling for Thai (AI might generate "Thai version readme:")
        self.language_patterns["th"] = []
        
        self.filename_map = {
            "zh": "README.zh.md",
            "zh-Hans": "README.zh.md",
            "zh-Hant": "README.zh-Hant.md",
            "en": "README.md",      # English README goes in root directory
            "ja": "README.ja.md",
            "ko": "README.ko.md",
            "fr": "README.fr.md",
            "de": "README.de.md",
            "es": "README.es.md",
            "it": "README.it.md",
            "pt": "README.pt.md",
            "pt-PT": "README.pt-PT.md",
            "ru": "README.ru.md",
            "th": "README.th.md",
            "vi": "README.vi.md",
            "hi": "README.hi.md",
            "ar": "README.ar.md",
            "tr": "README.tr.md",
            "pl": "README.pl.md",
            "nl": "README.nl.md",
            "sv": "README.sv.md",
            "da": "README.da.md",
            "no": "README.no.md",
            "nb": "README.nb.md",
            "fi": "README.fi.md",
            "cs": "README.cs.md",
            "sk": "README.sk.md",
            "hu": "README.hu.md",
            "ro": "README.ro.md",
            "bg": "README.bg.md",
            "hr": "README.hr.md",
            "sl": "README.sl.md",
            "et": "README.et.md",
            "lv": "README.lv.md",
            "lt": "README.lt.md",
            "mt": "README.mt.md",
            "el": "README.el.md",
            "ca": "README.ca.md",
            "eu": "README.eu.md",
            "gl": "README.gl.md",
            "af": "README.af.md",
            "zu": "README.zu.md",
            "xh": "README.xh.md",
            "st": "README.st.md",
            "sw": "README.sw.md",
            "yo": "README.yo.md",
            "ig": "README.ig.md",
            "ha": "README.ha.md",
            "am": "README.am.md",
            "or": "README.or.md",
            "bn": "README.bn.md",
            "gu": "README.gu.md",
            "pa": "README.pa.md",
            "te": "README.te.md",
            "kn": "README.kn.md",
            "ml": "README.ml.md",
            "ta": "README.ta.md",
            "si": "README.si.md",
            "my": "README.my.md",
            "km": "README.km.md",
            "lo": "README.lo.md",
            "ne": "README.ne.md",
            "ur": "README.ur.md",
            "fa": "README.fa.md",
            "ps": "README.ps.md",
            "sd": "README.sd.md",
            "he": "README.he.md",
            "yue": "README.yue.md"
        }
    
    def parse_multilingual_content(self, response_text: str, languages: Optional[List[str]] = None) -> ParsedReadme:
        """
        Parse multi-language README content
        
        Args:
            response_text: Generation response text (JSON format)
            languages: List of languages to parse, if None then parse all supported languages
            
        Returns:
            ParsedReadme: Parsing result object
        """
        if languages is None:
            # Directly use all supported language codes
            languages = ["en", "zh-Hans", "zh-Hant", "ja", "ko", "fr", "de", "es", "it", "pt", "pt-PT", "ru", "th", "vi", "hi", "ar", "tr", "pl", "nl", "sv", "da", "no", "nb", "fi", "cs", "sk", "hu", "ro", "bg", "hr", "sl", "et", "lv", "lt", "mt", "el", "ca", "eu", "gl", "af", "zu", "xh", "st", "sw", "yo", "ig", "ha", "am", "or", "bn", "gu", "pa", "te", "kn", "ml", "ta", "si", "my", "km", "lo", "ne", "ur", "fa", "ps", "sd", "he", "yue", "zh-Hant"]
        
        results = {}
        found_languages = []
        
        # Use new JSON extractor
        json_data, language_content = extract_json_content(response_text)
        
        if json_data:
            debug(f"🔍 Successfully extracted JSON data, contains {len(json_data)} keys")
            
            # Use extracted language content
            for lang_code, content in language_content.items():
                if lang_code in languages:
                    results[lang_code] = content
                    found_languages.append(lang_code)
                    debug(f"Successfully parsed {lang_code} language content")
            
            if results:
                debug(f"Successfully parsed {len(results)} languages")
                return ParsedReadme(
                    content=results,
                    languages=found_languages,
                    total_count=len(results)
                )
        else:
            error("Unable to extract JSON data")
            debug(f"Original response text: {response_text[:200]}...")
        
        if not results:
            warning("Failed to parse multi-language README content")
        
        return ParsedReadme(
            content=results,
            languages=found_languages,
            total_count=len(results)
        )
    
    def get_filename_for_language(self, language: str) -> str:
        """
        Get filename for specified language
        
        Args:
            language: Language name
            
        Returns:
            str: Corresponding filename
        """
        return self.filename_map.get(language, f"README.{language.lower()}.md")
    
    def get_supported_languages(self) -> List[str]:
        """
        Get list of supported languages for parsing
        
        Returns:
            List[str]: List of supported languages
        """
        return list(self.language_patterns.keys())
    
    def validate_content(self, content: str) -> bool:
        """
        Validate if content contains valid multi-language README format
        
        Args:
            content: Content to validate
            
        Returns:
            bool: Whether it contains valid multi-language README format
        """
        # Check if it contains at least one language marker
        for patterns in self.language_patterns.values():
            for pattern in patterns:
                if re.search(pattern, content, re.DOTALL):
                    return True
        return False
    
    def extract_language_sections(self, content: str) -> Dict[str, str]:
        """
        Extract content from all language sections
        
        Args:
            content: Content to parse
            
        Returns:
            Dict[str, str]: Language to content mapping
        """
        sections = {}
        
        for lang, patterns in self.language_patterns.items():
            for pattern in patterns:
                match = re.search(pattern, content, re.DOTALL)
                if match:
                    sections[lang] = match.group(1).strip()
                    break
        
        return sections
    
    def _map_json_key_to_language(self, json_key: str) -> Optional[str]:
        """
        Map JSON key to language code
        
        Args:
            json_key: Key name in JSON
            
        Returns:
            Optional[str]: Corresponding language code, returns None if unable to map
        """
        # JSON key to language code mapping
        json_key_map = {
            "English readme": "en",
            "Chinese readme": "zh", 
            "Japanese readme": "ja",
            "日本語 readme": "ja",  # Add Japanese variant
            "Korean readme": "ko",
            "French readme": "fr",
            "German readme": "de",
            "Spanish readme": "es",
            "Italian readme": "it",
            "Portuguese readme": "pt",
            "Russian readme": "ru",
            "Vietnamese readme": "vi",
            "Thai readme": "th",
            "Hindi readme": "hi",
            "Arabic readme": "ar",
            "Turkish readme": "tr",
            "Polish readme": "pl",
            "Dutch readme": "nl",
            "Swedish readme": "sv",
            "Danish readme": "da",
            "Norwegian readme": "no"
        }
        
        return json_key_map.get(json_key) 