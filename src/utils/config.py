"""
配置管理模块

负责管理项目的配置信息。
"""

import os
import yaml
from pathlib import Path
from typing import Any, Dict, Optional


class Config:
    """配置管理类"""
    
    def __init__(self, config_file: Optional[str] = None):
        """
        初始化配置管理器
        
        Args:
            config_file: 配置文件路径，如果为None则使用默认配置
        """
        self.config_file = config_file
        self._config = self._load_default_config()
        
        if config_file and Path(config_file).exists():
            self._load_config_file(config_file)
        
        # 从环境变量加载配置
        self._load_from_env()
    
    def _load_default_config(self) -> Dict[str, Any]:
        """加载默认配置"""
        return {
            "app": {
                "bot_app_key": "iIuhxDngAPmYRviQivBhDWVjxupvbeahuYivbmljFcNIyfHRcJdqLjjFTqYjwkBsuyhQMICCAbuEIfKzbhRelPxPZroXYEHzVoHpnuwcPnxErHdmzPGSUDCIiwkVtPkc",
                "visitor_biz_id": "202403130001"
            },
            "tencent_cloud": {
                "secret_id": "",
                "secret_key": "",
                "region": "ap-beijing",
                "service": "lke",
                "api_version": "2023-11-30"
            },
            "translation": {
                "default_languages": [
                    "中文", "English", "日本語", "한국어", "Français", 
                    "Deutsch", "Español", "Italiano", "Português", "Русский"
                ],
                "batch_size": 5,
                "timeout": 30
            },

            "sse": {
                "streaming_throttle": 1,
                "timeout": 60
            }
        }
    
    def _load_config_file(self, config_file: str):
        """从配置文件加载配置"""
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                file_config = yaml.safe_load(f)
                self._merge_config(file_config)
        except Exception as e:
            print(f"警告: 无法加载配置文件 {config_file}: {e}")
    
    def _load_from_env(self):
        """从环境变量加载配置"""
        env_mappings = {
            "DUOREADME_BOT_APP_KEY": ("app.bot_app_key",),
            "DUOREADME_VISITOR_BIZ_ID": ("app.visitor_biz_id",),
            "TENCENTCLOUD_SECRET_ID": ("tencent_cloud.secret_id",),
            "TENCENTCLOUD_SECRET_KEY": ("tencent_cloud.secret_key",),
            "TENCENTCLOUD_REGION": ("tencent_cloud.region",),


        }
        
        for env_var, config_path in env_mappings.items():
            value = os.environ.get(env_var)
            if value is not None:
                self.set_nested(config_path, value)
    
    def _merge_config(self, new_config: Dict[str, Any]):
        """合并配置"""
        def merge_dict(base: Dict[str, Any], update: Dict[str, Any]):
            for key, value in update.items():
                if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                    merge_dict(base[key], value)
                else:
                    base[key] = value
        
        merge_dict(self._config, new_config)
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        获取配置值
        
        Args:
            key: 配置键，支持点号分隔的嵌套键
            default: 默认值
            
        Returns:
            配置值
        """
        keys = key.split('.')
        value = self._config
        
        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default
    
    def set(self, key: str, value: Any):
        """
        设置配置值
        
        Args:
            key: 配置键，支持点号分隔的嵌套键
            value: 配置值
        """
        keys = key.split('.')
        config = self._config
        
        # 导航到父级
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        # 设置值
        config[keys[-1]] = value
    
    def set_nested(self, keys: tuple, value: Any):
        """
        设置嵌套配置值
        
        Args:
            keys: 键的元组
            value: 配置值
        """
        config = self._config
        
        # 导航到父级
        for key in keys[:-1]:
            if key not in config:
                config[key] = {}
            config = config[key]
        
        # 设置值
        config[keys[-1]] = value
    
    def save(self, config_file: Optional[str] = None):
        """
        保存配置到文件
        
        Args:
            config_file: 配置文件路径，如果为None则使用初始化时的路径
        """
        if config_file is None:
            config_file = self.config_file
        
        if config_file:
            try:
                with open(config_file, 'w', encoding='utf-8') as f:
                    yaml.dump(self._config, f, default_flow_style=False, allow_unicode=True)
                print(f"配置已保存到 {config_file}")
            except Exception as e:
                print(f"保存配置失败: {e}")
    
    def get_all(self) -> Dict[str, Any]:
        """
        获取所有配置
        
        Returns:
            所有配置的字典
        """
        return self._config.copy()
    
    def validate(self) -> bool:
        """
        验证配置的有效性
        
        Returns:
            配置是否有效
        """
        required_keys = [
            "app.bot_app_key",
            "app.visitor_biz_id"
        ]
        
        for key in required_keys:
            if not self.get(key):
                print(f"错误: 缺少必需的配置项 {key}")
                return False
        
        return True 