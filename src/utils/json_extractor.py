"""
JSON内容提取器

用于从各种响应格式中提取JSON内容。
"""

import re
import json
from typing import Dict, Any, Optional, Tuple


class JSONExtractor:
    """JSON内容提取器类"""
    
    @staticmethod
    def extract_json_from_response(response_text: str) -> Optional[Dict[str, Any]]:
        """
        从响应文本中提取JSON内容
        
        Args:
            response_text: 响应文本
            
        Returns:
            Optional[Dict[str, Any]]: 提取的JSON数据，如果提取失败则返回None
        """
        if not response_text or not response_text.strip():
            return None
            
        # 方法1: 尝试提取JSON代码块
        json_data = JSONExtractor._extract_json_code_block(response_text)
        if json_data:
            return json_data
            
        # 方法2: 尝试提取完整的JSON对象
        json_data = JSONExtractor._extract_complete_json_object(response_text)
        if json_data:
            return json_data
            
        # 方法3: 尝试修复和解析不完整的JSON
        json_data = JSONExtractor._extract_and_fix_incomplete_json(response_text)
        if json_data:
            return json_data
            
        return None
    
    @staticmethod
    def _extract_json_code_block(response_text: str) -> Optional[Dict[str, Any]]:
        """从代码块中提取JSON"""
        try:
            # 查找 ```json ... ``` 格式
            json_match = re.search(r'```json\s*(.*?)\s*```', response_text, re.DOTALL)
            if json_match:
                json_text = json_match.group(1).strip()
                return json.loads(json_text)
                
            # 查找 ``` ... ``` 格式（可能是JSON）
            code_match = re.search(r'```\s*(.*?)\s*```', response_text, re.DOTALL)
            if code_match:
                json_text = code_match.group(1).strip()
                # 检查是否看起来像JSON
                if json_text.startswith('{') and json_text.endswith('}'):
                    return json.loads(json_text)
        except (json.JSONDecodeError, AttributeError):
            pass
        return None
    
    @staticmethod
    def _extract_complete_json_object(response_text: str) -> Optional[Dict[str, Any]]:
        """提取完整的JSON对象"""
        try:
            # 查找第一个 { 和最后一个 }
            start = response_text.find('{')
            if start == -1:
                return None
                
            # 找到匹配的结束括号
            brace_count = 0
            end = -1
            for i in range(start, len(response_text)):
                if response_text[i] == '{':
                    brace_count += 1
                elif response_text[i] == '}':
                    brace_count -= 1
                    if brace_count == 0:
                        end = i + 1
                        break
            
            if end != -1:
                json_text = response_text[start:end]
                # 清理控制字符
                json_text = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', json_text)
                return json.loads(json_text)
        except (json.JSONDecodeError, IndexError):
            pass
        return None
    
    @staticmethod
    def _extract_and_fix_incomplete_json(response_text: str) -> Optional[Dict[str, Any]]:
        """提取并修复不完整的JSON"""
        try:
            # 查找JSON开始位置
            json_start = response_text.find('"English readme"')
            if json_start == -1:
                return None
                
            # 向前查找对象开始
            brace_start = response_text.rfind('{', 0, json_start)
            if brace_start == -1:
                return None
                
            # 尝试找到匹配的结束括号
            brace_count = 0
            brace_end = -1
            for i in range(brace_start, len(response_text)):
                if response_text[i] == '{':
                    brace_count += 1
                elif response_text[i] == '}':
                    brace_count -= 1
                    if brace_count == 0:
                        brace_end = i + 1
                        break
            
            if brace_end == -1:
                # 如果没有找到匹配的结束括号，尝试修复
                return JSONExtractor._fix_truncated_json(response_text[brace_start:])
            
            json_text = response_text[brace_start:brace_end]
            # 清理控制字符
            json_text = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', json_text)
            return json.loads(json_text)
            
        except (json.JSONDecodeError, IndexError):
            return None
    
    @staticmethod
    def _fix_truncated_json(json_text: str) -> Optional[Dict[str, Any]]:
        """修复被截断的JSON"""
        try:
            # 清理控制字符
            json_text = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', json_text)
            
            # 如果JSON被截断，尝试添加必要的结束部分
            if not json_text.endswith('}'):
                # 查找最后一个完整的键值对
                last_comma = json_text.rfind(',')
                if last_comma != -1:
                    # 移除最后一个逗号并添加结束括号
                    json_text = json_text[:last_comma] + '}'
                else:
                    # 如果没有逗号，直接添加结束括号
                    json_text += '}'
            
            return json.loads(json_text)
        except (json.JSONDecodeError, IndexError):
            return None
    
    @staticmethod
    def extract_language_content(json_data: Dict[str, Any]) -> Dict[str, str]:
        """
        从JSON数据中提取语言内容
        
        Args:
            json_data: JSON数据
            
        Returns:
            Dict[str, str]: 语言代码到内容的映射
        """
        # 支持多种可能的键名格式
        language_map = {
            # 标准语言代码
            "zh-Hans": "zh-Hans",
            "zh-Hant": "zh-Hant", 
            "en": "en",
            "ja": "ja",
            "ko": "ko",
            "fr": "fr",
            "de": "de",
            "es": "es",
            "it": "it",
            "pt": "pt",
            "ru": "ru",
            "th": "th",
            "hi": "hi",
            "ar": "ar",
            "vi": "vi",
            "tr": "tr",
            "pl": "pl",
            "nl": "nl",
            "sv": "sv",
            "da": "da",
            "no": "no",
            
            # 语言名称（英文）
            "English": "en",
            "Chinese": "zh-Hans",
            "Japanese": "ja",
            "Korean": "ko",
            "French": "fr",
            "German": "de",
            "Spanish": "es",
            "Italian": "it",
            "Portuguese": "pt",
            "Russian": "ru",
            "Thai": "th",
            "Hindi": "hi",
            "Arabic": "ar",
            "Vietnamese": "vi",
            "Turkish": "tr",
            "Polish": "pl",
            "Dutch": "nl",
            "Swedish": "sv",
            "Danish": "da",
            "Norwegian": "no",
            
            # 带 "readme" 后缀的格式
            "English readme": "en",
            "Chinese readme": "zh-Hans", 
            "Japanese readme": "ja",
            "Korean readme": "ko",
            "French readme": "fr",
            "German readme": "de",
            "Spanish readme": "es",
            "Italian readme": "it",
            "Portuguese readme": "pt",
            "Russian readme": "ru",
            "Thai readme": "th",
            "Hindi readme": "hi",
            "Arabic readme": "ar",
            "Vietnamese readme": "vi",
            "Turkish readme": "tr",
            "Polish readme": "pl",
            "Dutch readme": "nl",
            "Swedish readme": "sv",
            "Danish readme": "da",
            "Norwegian readme": "no",
            
            # 其他可能的格式
            "日本語 readme": "ja",
            "中文 readme": "zh-Hans",
            "한국어 readme": "ko",
            "Français readme": "fr",
            "Deutsch readme": "de",
            "Español readme": "es",
            "Italiano readme": "it",
            "Português readme": "pt",
            "Русский readme": "ru",
            "ไทย readme": "th",
            "हिन्दी readme": "hi",
            "العربية readme": "ar",
            "Tiếng Việt readme": "vi",
            "Türkçe readme": "tr",
            "Polski readme": "pl",
            "Nederlands readme": "nl",
            "Svenska readme": "sv",
            "Dansk readme": "da",
            "Norsk readme": "no"
        }
        
        results = {}
        for key, content in json_data.items():
            # 尝试直接匹配键名
            lang_code = language_map.get(key)
            if lang_code and content and str(content).strip():
                results[lang_code] = str(content).strip()
                continue
            
            # 如果直接匹配失败，尝试标准化键名
            normalized_key = key.strip().lower()
            for map_key, map_value in language_map.items():
                if normalized_key == map_key.lower():
                    results[map_value] = str(content).strip()
                    break
        
        return results


def extract_json_content(response_text: str) -> Tuple[Optional[Dict[str, Any]], Dict[str, str]]:
    """
    从响应文本中提取JSON内容并解析语言内容
    
    Args:
        response_text: 响应文本
        
    Returns:
        Tuple[Optional[Dict[str, Any]], Dict[str, str]]: (JSON数据, 语言内容映射)
    """
    extractor = JSONExtractor()
    json_data = extractor.extract_json_from_response(response_text)
    
    if json_data:
        language_content = extractor.extract_language_content(json_data)
        return json_data, language_content
    else:
        return None, {} 