"""
Translation providers module

Provides different translation service providers.
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ...utils.config import Config

from .base import TranslationProvider
from .tencent_provider import TencentProvider
from .siliconflow_provider import SiliconFlowProvider


def get_provider(config: "Config") -> TranslationProvider:
    """
    Get translation provider based on configuration
    
    Args:
        config: Configuration object
        
    Returns:
        TranslationProvider: Translation provider instance
    """
    provider_name = config.get("provider", "tencent")
    
    if provider_name == "siliconflow":
        return SiliconFlowProvider(config)
    else:
        return TencentProvider(config)


__all__ = [
    "TranslationProvider",
    "TencentProvider", 
    "SiliconFlowProvider",
    "get_provider"
]
