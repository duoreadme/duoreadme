"""
类型定义模块

定义项目中使用的所有数据结构和类型。
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Any


@dataclass
class TranslationRequest:
    """翻译请求数据类"""
    content: str
    languages: List[str]
    bot_app_key: str
    visitor_biz_id: str
    additional_params: Optional[Dict[str, Any]] = None


@dataclass
class TranslationResponse:
    """翻译响应数据类"""
    success: bool
    content: str = ""
    languages: List[str] = None
    raw_response: str = ""
    error: str = ""
    
    def __post_init__(self):
        if self.languages is None:
            self.languages = []


@dataclass
class ParsedReadme:
    """解析后的README数据类"""
    content: Dict[str, str]
    languages: List[str]
    total_count: int


@dataclass
class GenerationResult:
    """生成结果数据类"""
    saved_files: List[Dict[str, Any]]
    failed_files: List[Dict[str, Any]]
    total_saved: int
    total_failed: int


@dataclass
class Config:
    """配置数据类"""
    bot_app_key: str = ""
    visitor_biz_id: str = ""
    tencent_secret_id: str = ""
    tencent_secret_key: str = ""
    default_languages: List[str] = None
    
    def __post_init__(self):
        if self.default_languages is None:
            self.default_languages = [
                "中文", "English", "日本語", "한국어", "Français", 
                "Deutsch", "Español", "Italiano", "Português", "Русский"
            ]


@dataclass
class FileInfo:
    """文件信息数据类"""
    language: str
    filename: str
    filepath: str
    size: int
    created_time: Optional[str] = None
    modified_time: Optional[str] = None


@dataclass
class ProjectInfo:
    """项目信息数据类"""
    name: str
    path: str
    readme_path: Optional[str] = None
    src_path: Optional[str] = None
    files: List[str] = None
    
    def __post_init__(self):
        if self.files is None:
            self.files = [] 