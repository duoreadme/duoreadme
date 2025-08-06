"""
Logging module

Provides unified logging configuration and management.
"""

import logging
import sys
from typing import Optional


class Logger:
    """Log manager class"""
    
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
        """Set up logging configuration"""
        # Create logger
        self._logger = logging.getLogger('duoreadme')
        # Default to INFO level, don't output DEBUG content
        self._logger.setLevel(logging.INFO)
        
        # Clear existing handlers
        self._logger.handlers.clear()
        
        # Create console handler
        console_handler = logging.StreamHandler(sys.stdout)
        # Default to INFO level
        console_handler.setLevel(logging.INFO)
        
        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        console_handler.setFormatter(formatter)
        
        # Add handler to logger
        self._logger.addHandler(console_handler)
    
    def debug(self, message: str):
        """Output DEBUG level log"""
        self._logger.debug(message)
    
    def info(self, message: str):
        """Output INFO level log"""
        self._logger.info(message)
    
    def warning(self, message: str):
        """Output WARNING level log"""
        self._logger.warning(message)
    
    def error(self, message: str):
        """Output ERROR level log"""
        self._logger.error(message)
    
    def critical(self, message: str):
        """Output CRITICAL level log"""
        self._logger.critical(message)
    
    def set_level(self, level: str):
        """Set log level"""
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
        """Enable debug mode, output DEBUG level logs"""
        self.set_level('DEBUG')
    
    def disable_debug(self):
        """Disable debug mode, only output INFO and above level logs"""
        self.set_level('INFO')
    
    def get_logger(self) -> logging.Logger:
        """Get original logger object"""
        return self._logger


# Global log instance
logger = Logger()


def get_logger() -> Logger:
    """Get log instance"""
    return logger


def debug(message: str):
    """Output DEBUG level log"""
    logger.debug(message)


def info(message: str):
    """Output INFO level log"""
    logger.info(message)


def warning(message: str):
    """Output WARNING level log"""
    logger.warning(message)


def error(message: str):
    """Output ERROR level log"""
    logger.error(message)


def critical(message: str):
    """Output CRITICAL level log"""
    logger.critical(message)


def enable_debug():
    """Enable debug mode"""
    logger.enable_debug()


def disable_debug():
    """Disable debug mode"""
    logger.disable_debug() 