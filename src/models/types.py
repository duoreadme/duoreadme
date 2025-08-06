"""
Type definition module

Defines all data structures and types used in the project.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Any


@dataclass
class TranslationRequest:
    """Generation request data class"""
    content: str
    languages: List[str]
    bot_app_key: str
    visitor_biz_id: str
    additional_params: Optional[Dict[str, Any]] = None


@dataclass
class TranslationResponse:
    """Generation response data class"""
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
    """Parsed README data class"""
    content: Dict[str, str]
    languages: List[str]
    total_count: int


@dataclass
class GenerationResult:
    """Generation result data class"""
    saved_files: List[Dict[str, Any]]
    failed_files: List[Dict[str, Any]]
    total_saved: int
    total_failed: int


@dataclass
class Config:
    """Configuration data class"""
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
    """File information data class"""
    language: str
    filename: str
    filepath: str
    size: int
    created_time: Optional[str] = None
    modified_time: Optional[str] = None


@dataclass
class ProjectInfo:
    """Project information data class"""
    name: str
    path: str
    readme_path: Optional[str] = None
    src_path: Optional[str] = None
    files: List[str] = None
    
    def __post_init__(self):
        if self.files is None:
            self.files = [] 