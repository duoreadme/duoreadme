"""
DuoReadme - 多语言 README 生成工具

一个强大的CLI工具，用于将项目代码和README自动生成多种语言并生成规范化的多语言文档。
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