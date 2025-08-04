"""
CLI工具模块

提供命令行界面工具。
"""

from .main import main, cli
from .commands import translate_command, config_command

__all__ = ["main", "cli", "translate_command", "config_command"] 