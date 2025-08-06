"""
内容解析器模块

负责解析生成响应中的多语言README内容。
"""

import re
from typing import Dict, List, Optional
from ..models.types import ParsedReadme
from ..utils.json_extractor import extract_json_content
from ..utils.logger import debug, info, warning, error


class Parser:
    """解析器类，负责解析多语言README内容"""
    
    def __init__(self):
        """初始化解析器"""
        # 只保留JSON格式解析，移除正则表达式模式
        self.language_patterns = {}
        
        # 特殊处理泰语（AI可能生成"泰语版本readme:"）
        self.language_patterns["th"] = []
        
        self.filename_map = {
            "zh": "README.zh.md",
            "zh-Hans": "README.zh.md",
            "zh-Hant": "README.zh-Hant.md",
            "en": "README.md",      # 英文README放在根目录
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
        解析多语言README内容
        
        Args:
            response_text: 生成响应文本（JSON格式）
            languages: 要解析的语言列表，如果为None则解析所有支持的语言
            
        Returns:
            ParsedReadme: 解析结果对象
        """
        if languages is None:
            # 直接使用所有支持的语言代码
            languages = ["en", "zh-Hans", "zh-Hant", "ja", "ko", "fr", "de", "es", "it", "pt", "pt-PT", "ru", "th", "vi", "hi", "ar", "tr", "pl", "nl", "sv", "da", "no", "nb", "fi", "cs", "sk", "hu", "ro", "bg", "hr", "sl", "et", "lv", "lt", "mt", "el", "ca", "eu", "gl", "af", "zu", "xh", "st", "sw", "yo", "ig", "ha", "am", "or", "bn", "gu", "pa", "te", "kn", "ml", "ta", "si", "my", "km", "lo", "ne", "ur", "fa", "ps", "sd", "he", "yue", "zh-Hant"]
        
        results = {}
        found_languages = []
        
        # 使用新的JSON提取器
        json_data, language_content = extract_json_content(response_text)
        
        if json_data:
            debug(f"🔍 成功提取JSON数据，包含 {len(json_data)} 个键")
            
            # 使用提取的语言内容
            for lang_code, content in language_content.items():
                if lang_code in languages:
                    results[lang_code] = content
                    found_languages.append(lang_code)
                    debug(f"✅ 成功解析 {lang_code} 语言内容")
            
            if results:
                debug(f"✅ 成功解析 {len(results)} 种语言")
                return ParsedReadme(
                    content=results,
                    languages=found_languages,
                    total_count=len(results)
                )
        else:
            error("❌ 无法提取JSON数据")
            debug(f"🔍 原始响应文本: {response_text[:200]}...")
        
        if not results:
            warning("⚠️  未能解析到多语言 README 内容")
        
        return ParsedReadme(
            content=results,
            languages=found_languages,
            total_count=len(results)
        )
    
    def get_filename_for_language(self, language: str) -> str:
        """
        获取指定语言对应的文件名
        
        Args:
            language: 语言名称
            
        Returns:
            str: 对应的文件名
        """
        return self.filename_map.get(language, f"README.{language.lower()}.md")
    
    def get_supported_languages(self) -> List[str]:
        """
        获取支持解析的语言列表
        
        Returns:
            List[str]: 支持的语言列表
        """
        return list(self.language_patterns.keys())
    
    def validate_content(self, content: str) -> bool:
        """
        验证内容是否包含有效的多语言README格式
        
        Args:
            content: 要验证的内容
            
        Returns:
            bool: 是否包含有效的多语言README格式
        """
        # 检查是否包含至少一个语言标记
        for patterns in self.language_patterns.values():
            for pattern in patterns:
                if re.search(pattern, content, re.DOTALL):
                    return True
        return False
    
    def extract_language_sections(self, content: str) -> Dict[str, str]:
        """
        提取所有语言部分的内容
        
        Args:
            content: 要解析的内容
            
        Returns:
            Dict[str, str]: 语言到内容的映射
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
        将JSON键映射到语言代码
        
        Args:
            json_key: JSON中的键名
            
        Returns:
            Optional[str]: 对应的语言代码，如果无法映射则返回None
        """
        # JSON键到语言代码的映射
        json_key_map = {
            "English readme": "en",
            "Chinese readme": "zh", 
            "Japanese readme": "ja",
            "日本語 readme": "ja",  # 添加日语变体
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