"""
腾讯云服务模块

提供腾讯云API的集成服务。
"""

import os
from typing import Dict, Any, Optional
from tencentcloud.common.common_client import CommonClient
from tencentcloud.common import credential
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from ..utils.config import Config
from ..utils.logger import debug, info, warning, error


class TencentCloudService:
    """腾讯云服务类"""
    
    def __init__(self, config: Config):
        """
        初始化腾讯云服务
        
        Args:
            config: 配置对象
        """
        self.config = config
        self._service = "lke"
        self._api_version = "2023-11-30"
        debug("腾讯云服务初始化完成")
    
    def get_token(self, secret: Dict[str, str], profile: Dict[str, str], region: str, params: Dict[str, Any]) -> str:
        """
        获取腾讯云令牌
        
        Args:
            secret: 密钥信息字典
            profile: 配置信息字典
            region: 区域字符串
            params: 请求参数
            
        Returns:
            str: 令牌字符串，失败时返回空字符串
        """
        debug(f"开始获取腾讯云令牌: profile={profile}, region={region}")
        
        try:
            # 获取密钥信息
            secret_id = secret.get("secret_id", "")
            secret_key = secret.get("secret_key", "")
            
            # 如果secret中没有提供，则从配置中获取
            if not secret_id:
                secret_id = self.config.get("tencent_cloud.secret_id", "")
            if not secret_key:
                secret_key = self.config.get("tencent_cloud.secret_key", "")
            
            debug("腾讯云凭证配置完成")
            
            # 创建凭证
            cred = credential.Credential(secret_id, secret_key)
            
            # 配置HTTP配置
            http_profile = HttpProfile()
            domain = profile.get("domain", "")
            scheme = profile.get("scheme", "https")
            method = profile.get("method", "POST")
            
            http_profile.rootDomain = domain
            http_profile.scheme = scheme
            http_profile.reqMethod = method
            
            debug(f"HTTP配置: domain={domain}, scheme={scheme}, method={method}")
            
            # 创建客户端配置
            client_profile = ClientProfile()
            client_profile.httpProfile = http_profile
            
            # 实例化通用客户端
            common_client = CommonClient(
                self._service, 
                self._api_version, 
                cred, 
                region, 
                profile=client_profile
            )
            
            debug("腾讯云客户端创建完成，开始调用API")
            
            # 调用API
            resp = common_client.call_json("GetWsToken", params)
            debug("腾讯云API调用成功")
            
            # 提取令牌
            token = ""
            if "Response" in resp and "Token" in resp["Response"]:
                token = resp["Response"]["Token"]
                debug("成功提取令牌")
            else:
                warning("API响应中未找到Token字段")
            
            return token
            
        except TencentCloudSDKException as err:
            error(f"腾讯云SDK异常: {err}")
            return ""
        except Exception as err:
            error(f"获取令牌失败: {err}")
            return ""
    
    def validate_credentials(self) -> bool:
        """
        验证腾讯云凭证是否有效
        
        Returns:
            bool: 凭证是否有效
        """
        secret_id = self.config.get("tencent_cloud.secret_id", "")
        secret_key = self.config.get("tencent_cloud.secret_key", "")
        
        if not secret_id or not secret_key:
            print("错误: 缺少腾讯云凭证")
            return False
        
        return True
    
    def get_default_region(self) -> str:
        """
        获取默认区域
        
        Returns:
            str: 默认区域
        """
        return self.config.get("tencent_cloud.region", "ap-beijing")
    
    def get_service_info(self) -> Dict[str, str]:
        """
        获取服务信息
        
        Returns:
            Dict[str, str]: 服务信息
        """
        return {
            "service": self._service,
            "api_version": self._api_version,
            "region": self.get_default_region()
        } 