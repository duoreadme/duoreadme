"""
Data models module

Contains all data models and type definitions used in the project.
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