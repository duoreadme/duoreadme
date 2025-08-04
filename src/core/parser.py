"""
内容解析器模块

负责解析翻译响应中的多语言README内容。
"""

import re
from typing import Dict, List, Optional
from ..models.types import ParsedReadme


class Parser:
    """解析器类，负责解析多语言README内容"""
    
    def __init__(self):
        """初始化解析器"""
        # 支持多种格式的语言模式
        self.language_patterns = {
            # 标准格式: ### 中文
            "zh": [
                r"### 中文\s*\n(.*?)(?=\n### |$)",
                r"中文版本readme：\s*\n(.*?)(?=\n(?:英文版本|中文版本|泰语版本|日文版本|韩文版本|法文版本|德文版本|西班牙文版本|意大利文版本|葡萄牙文版本|俄文版本)readme|$)"
            ],
            "en": [
                r"### English\s*\n(.*?)(?=\n### |$)",
                r"英文版本readme:\s*\n(.*?)(?=\n(?:英文版本|中文版本|泰语版本|日文版本|韩文版本|法文版本|德文版本|西班牙文版本|意大利文版本|葡萄牙文版本|俄文版本)readme|$)"
            ],
            "ja": [
                r"### 日本語\s*\n(.*?)(?=\n### |$)",
                r"日文版本readme:\s*\n(.*?)(?=\n(?:英文版本|中文版本|泰语版本|日文版本|韩文版本|法文版本|德文版本|西班牙文版本|意大利文版本|葡萄牙文版本|俄文版本)readme|$)",
                r"日本語版本readme：\s*\n(.*?)(?=\n(?:英文版本|中文版本|泰语版本|日文版本|韩文版本|法文版本|德文版本|西班牙文版本|意大利文版本|葡萄牙文版本|俄文版本)readme|$)",
                r"日本語版本readme：\s*\n(.*?)$",
                r"日本語版本readme:\s*\n(.*?)(?=\n(?:英文版本|中文版本|泰语版本|日文版本|韩文版本|法文版本|德文版本|西班牙文版本|意大利文版本|葡萄牙文版本|俄文版本)readme|$)",
                r"日本語版本readme:\s*\n(.*?)$"
            ],
            "ko": [
                r"### 한국어\s*\n(.*?)(?=\n### |$)",
                r"韩文版本readme:\s*\n(.*?)(?=\n(?:英文版本|中文版本|泰语版本|日文版本|韩文版本|法文版本|德文版本|西班牙文版本|意大利文版本|葡萄牙文版本|俄文版本)readme|$)"
            ],
            "fr": [
                r"### Français\s*\n(.*?)(?=\n### |$)",
                r"法文版本readme:\s*\n(.*?)(?=\n(?:英文版本|中文版本|泰语版本|日文版本|韩文版本|法文版本|德文版本|西班牙文版本|意大利文版本|葡萄牙文版本|俄文版本)readme|$)"
            ],
            "de": [
                r"### Deutsch\s*\n(.*?)(?=\n### |$)",
                r"德文版本readme:\s*\n(.*?)(?=\n(?:英文版本|中文版本|泰语版本|日文版本|韩文版本|法文版本|德文版本|西班牙文版本|意大利文版本|葡萄牙文版本|俄文版本)readme|$)"
            ],
            "es": [
                r"### Español\s*\n(.*?)(?=\n### |$)",
                r"西班牙文版本readme:\s*\n(.*?)(?=\n(?:英文版本|中文版本|泰语版本|日文版本|韩文版本|法文版本|德文版本|西班牙文版本|意大利文版本|葡萄牙文版本|俄文版本)readme|$)"
            ],
            "it": [
                r"### Italiano\s*\n(.*?)(?=\n### |$)",
                r"意大利文版本readme:\s*\n(.*?)(?=\n(?:英文版本|中文版本|泰语版本|日文版本|韩文版本|法文版本|德文版本|西班牙文版本|意大利文版本|葡萄牙文版本|俄文版本)readme|$)"
            ],
            "pt": [
                r"### Português\s*\n(.*?)(?=\n### |$)",
                r"葡萄牙文版本readme:\s*\n(.*?)(?=\n(?:英文版本|中文版本|泰语版本|日文版本|韩文版本|法文版本|德文版本|西班牙文版本|意大利文版本|葡萄牙文版本|俄文版本)readme|$)"
            ],
            "ru": [
                r"### Русский\s*\n(.*?)(?=\n### |$)",
                r"俄文版本readme:\s*\n(.*?)(?=\n(?:英文版本|中文版本|泰语版本|日文版本|韩文版本|法文版本|德文版本|西班牙文版本|意大利文版本|葡萄牙文版本|俄文版本)readme|$)"
            ]
        }
        
        # 特殊处理泰语（AI可能生成"泰语版本readme:"）
        self.language_patterns["th"] = [
            r"### 泰语\s*\n(.*?)(?=\n### |$)",
            r"泰语版本readme:\s*\n(.*?)(?=\n(?:英文版本|中文版本|泰语版本|日文版本|韩文版本|法文版本|德文版本|西班牙文版本|意大利文版本|葡萄牙文版本|俄文版本)readme|$)"
        ]
        
        self.filename_map = {
            "zh": "README.zh.md",
            "en": "README.en.md", 
            "ja": "README.ja.md",
            "ko": "README.ko.md",
            "fr": "README.fr.md",
            "de": "README.de.md",
            "es": "README.es.md",
            "it": "README.it.md",
            "pt": "README.pt.md",
            "ru": "README.ru.md",
            "th": "README.th.md"
        }
    
    def parse_multilingual_content(self, response_text: str, languages: Optional[List[str]] = None) -> ParsedReadme:
        """
        解析多语言README内容
        
        Args:
            response_text: 翻译响应文本
            languages: 要解析的语言列表，如果为None则解析所有支持的语言
            
        Returns:
            ParsedReadme: 解析结果对象
        """
        if languages is None:
            languages = list(self.language_patterns.keys())
        
        results = {}
        found_languages = []
        
        print("正在解析多语言 README...")
        
        for lang in languages:
            if lang in self.language_patterns:
                patterns = self.language_patterns[lang]
                content = None
                
                # 尝试所有模式
                for pattern in patterns:
                    match = re.search(pattern, response_text, re.DOTALL)
                    if match:
                        content = match.group(1).strip()
                        if content:
                            results[lang] = content
                            found_languages.append(lang)
                            print(f"找到 {lang} 版本")
                            break
        
        if not results:
            print("未能解析到多语言 README 内容")
            # 调试：显示响应内容的前500个字符
            print(f"响应内容预览: {response_text[:500]}...")
        else:
            print(f"成功解析了 {len(results)} 种语言的 README")
        
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