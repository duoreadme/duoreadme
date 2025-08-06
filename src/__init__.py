"""
DuoReadme - Multilingual README Generation Tool

A powerful CLI tool for automatically generating project code and README into multiple languages and creating standardized multilingual documentation.
"""

__version__ = "1.0.0"
__author__ = "DuoReadme Team"

from .core.translator import Translator
from .core.parser import Parser
from .core.generator import Generator

__all__ = [
    "Translator",
    "Parser", 
    "Generator",
    "__version__",
    "__author__",
    "__email__"
] 