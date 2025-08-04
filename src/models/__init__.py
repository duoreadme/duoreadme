"""
数据模型模块

包含项目中使用的所有数据模型和类型定义。
"""

from .types import (
    TranslationRequest,
    TranslationResponse,
    ParsedReadme,
    GenerationResult
)

__all__ = [
    "TranslationRequest",
    "TranslationResponse", 
    "ParsedReadme",
    "GenerationResult"
] 