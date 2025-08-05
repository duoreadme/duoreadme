"""
日志模块

提供统一的日志配置和管理。
"""

import logging
import sys
from typing import Optional


class Logger:
    """日志管理器类"""
    
    _instance = None
    _logger = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if self._logger is None:
            self._setup_logger()
    
    def _setup_logger(self):
        """设置日志配置"""
        # 创建logger
        self._logger = logging.getLogger('duoreadme')
        # 默认设置为 INFO 级别，不输出 DEBUG 内容
        self._logger.setLevel(logging.INFO)
        
        # 清除现有的处理器
        self._logger.handlers.clear()
        
        # 创建控制台处理器
        console_handler = logging.StreamHandler(sys.stdout)
        # 默认设置为 INFO 级别
        console_handler.setLevel(logging.INFO)
        
        # 创建格式化器
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        console_handler.setFormatter(formatter)
        
        # 添加处理器到logger
        self._logger.addHandler(console_handler)
    
    def debug(self, message: str):
        """输出DEBUG级别日志"""
        self._logger.debug(message)
    
    def info(self, message: str):
        """输出INFO级别日志"""
        self._logger.info(message)
    
    def warning(self, message: str):
        """输出WARNING级别日志"""
        self._logger.warning(message)
    
    def error(self, message: str):
        """输出ERROR级别日志"""
        self._logger.error(message)
    
    def critical(self, message: str):
        """输出CRITICAL级别日志"""
        self._logger.critical(message)
    
    def set_level(self, level: str):
        """设置日志级别"""
        level_map = {
            'DEBUG': logging.DEBUG,
            'INFO': logging.INFO,
            'WARNING': logging.WARNING,
            'ERROR': logging.ERROR,
            'CRITICAL': logging.CRITICAL
        }
        
        if level.upper() in level_map:
            self._logger.setLevel(level_map[level.upper()])
            for handler in self._logger.handlers:
                handler.setLevel(level_map[level.upper()])
    
    def enable_debug(self):
        """启用调试模式，输出 DEBUG 级别日志"""
        self.set_level('DEBUG')
    
    def disable_debug(self):
        """禁用调试模式，只输出 INFO 及以上级别日志"""
        self.set_level('INFO')
    
    def get_logger(self) -> logging.Logger:
        """获取原始logger对象"""
        return self._logger


# 全局日志实例
logger = Logger()


def get_logger() -> Logger:
    """获取日志实例"""
    return logger


def debug(message: str):
    """输出DEBUG级别日志"""
    logger.debug(message)


def info(message: str):
    """输出INFO级别日志"""
    logger.info(message)


def warning(message: str):
    """输出WARNING级别日志"""
    logger.warning(message)


def error(message: str):
    """输出ERROR级别日志"""
    logger.error(message)


def critical(message: str):
    """输出CRITICAL级别日志"""
    logger.critical(message)


def enable_debug():
    """启用调试模式"""
    logger.enable_debug()


def disable_debug():
    """禁用调试模式"""
    logger.disable_debug() 