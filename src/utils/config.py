"""
Configuration management module

Responsible for managing project configuration information.
"""

import os
import yaml
from pathlib import Path
from typing import Any, Dict, Optional


class Config:
    """Configuration management class"""
    
    def __init__(self, config_file: Optional[str] = None):
        """
        Initialize configuration manager
        
        Args:
            config_file: Configuration file path, if None then try to load default configuration file
        """
        self.config_file = config_file
        self._config = self._load_default_config()
        
        # Load configuration file
        if config_file and Path(config_file).exists():
            self._load_config_file(config_file)
        else:
            # If no configuration file specified, try to load default configuration file
            default_config_files = ["config.yaml", "config.yml", ".config.yaml"]
            for default_file in default_config_files:
                if Path(default_file).exists():
                    self._load_config_file(default_file)
                    self.config_file = default_file
                    break
        
        # Load configuration from environment variables
        self._load_from_env()
    
    def _load_default_config(self) -> Dict[str, Any]:
        """Load default configuration"""
        return {
            "app": {
                "bot_app_key": "",
                "visitor_biz_id": ""
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
                    "af", "am", "ar", "as", "az", "ba", "bg", "bho", "bn", "bo", "brx", "bs", "ca", "cs", "cy", "da", "de", "doi", "dsb", "dv", "el", "en", "es", "et", "eu", "fa", "fi", "fil", "fj", "fo", "fr", "fr-CA", "ga", "gl", "gom", "gu", "ha", "he", "hi", "hne", "hr", "hsb", "ht", "hu", "hy", "id", "ig", "ikt", "is", "it", "iu", "iu-Latin", "ja", "ka", "kk", "km", "kmr", "kn", "ko", "ks", "ku", "ky", "ln", "lo", "lt", "lug", "lv", "lzh", "mai", "mg", "mi", "mk", "ml", "mn-Cyrl", "mn-Mong", "mni", "mr", "ms", "mt", "mww", "my", "nb", "ne", "nl", "nso", "nya", "or", "otq", "pa", "pl", "prs", "ps", "pt", "pt-PT", "ro", "ru", "run", "rw", "sd", "si", "sk", "sl", "sm", "sn", "so", "sq", "sr-Cyrl", "sr-Latin", "st", "sv", "sw", "ta", "te", "th", "ti", "tk", "tlh-Latin", "tlh-Piqd", "tn", "to", "tr", "tt", "ty", "ug", "uk", "ur", "uz", "vi", "xh", "yo", "yua", "yue", "zh-Hans", "zh-Hant", "zu"
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
        """Load configuration from configuration file"""
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                file_config = yaml.safe_load(f)
                self._merge_config(file_config)
        except Exception as e:
            print(f"Warning: Unable to load configuration file {config_file}: {e}")
    
    def _load_from_env(self):
        """Load configuration from environment variables"""
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
        """Merge configuration"""
        def merge_dict(base: Dict[str, Any], update: Dict[str, Any]):
            for key, value in update.items():
                if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                    merge_dict(base[key], value)
                else:
                    base[key] = value
        
        merge_dict(self._config, new_config)
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value
        
        Args:
            key: Configuration key, supports dot-separated nested keys
            default: Default value
            
        Returns:
            Configuration value
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
        Set configuration value
        
        Args:
            key: Configuration key, supports dot-separated nested keys
            value: Configuration value
        """
        keys = key.split('.')
        config = self._config
        
        # Navigate to parent level
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        # Set value
        config[keys[-1]] = value
    
    def set_nested(self, keys: tuple, value: Any):
        """
        Set nested configuration value
        
        Args:
            keys: Tuple of keys
            value: Configuration value
        """
        config = self._config
        
        # Navigate to parent level
        for key in keys[:-1]:
            if key not in config:
                config[key] = {}
            config = config[key]
        
        # Set value
        config[keys[-1]] = value
    
    def save(self, config_file: Optional[str] = None):
        """
        Save configuration to file
        
        Args:
            config_file: Configuration file path, if None then use path from initialization
        """
        if config_file is None:
            config_file = self.config_file
        
        if config_file:
            try:
                with open(config_file, 'w', encoding='utf-8') as f:
                    yaml.dump(self._config, f, default_flow_style=False, allow_unicode=True)
                print(f"Configuration saved to {config_file}")
            except Exception as e:
                print(f"Failed to save configuration: {e}")
    
    def get_all(self) -> Dict[str, Any]:
        """
        Get all configuration
        
        Returns:
            Dictionary of all configuration
        """
        return self._config.copy()
    
    def validate(self) -> bool:
        """
        Validate configuration validity
        
        Returns:
            Whether configuration is valid
        """
        required_keys = [
            "app.bot_app_key",
            # "app.visitor_biz_id"
        ]
        
        missing_keys = []
        for key in required_keys:
            value = self.get(key)
            if not value or value.startswith("your_") or value == "":
                missing_keys.append(key)
        
        if missing_keys:
            print("Error: The following required configuration items are not properly set:")
            for key in missing_keys:
                print(f"  - {key}")
            print("\nPlease edit the config.yaml file and fill in the correct configuration values.")
            return False
        
        return True 