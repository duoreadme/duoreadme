"""
Tencent Cloud service module

Provides Tencent Cloud API integration services.
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
    """Tencent Cloud service class"""
    
    def __init__(self, config: Config):
        """
        Initialize Tencent Cloud service
        
        Args:
            config: Configuration object
        """
        self.config = config
        self._service = "lke"
        self._api_version = "2023-11-30"
        debug("Tencent Cloud service initialized")
    
    def get_token(self, secret: Dict[str, str], profile: Dict[str, str], region: str, params: Dict[str, Any]) -> str:
        """
        Get Tencent Cloud token
        
        Args:
            secret: Secret information dictionary
            profile: Configuration information dictionary
            region: Region string
            params: Request parameters
            
        Returns:
            str: Token string, returns empty string on failure
        """
        debug(f"Starting to get Tencent Cloud token: profile={profile}, region={region}")
        
        try:
            # Get secret information
            secret_id = secret.get("secret_id", "")
            secret_key = secret.get("secret_key", "")
            
            # If not provided in secret, get from configuration
            if not secret_id:
                secret_id = self.config.get("tencent_cloud.secret_id", "")
            if not secret_key:
                secret_key = self.config.get("tencent_cloud.secret_key", "")
            
            debug("Tencent Cloud credentials configured")
            
            # Create credentials
            cred = credential.Credential(secret_id, secret_key)
            
            # Configure HTTP configuration
            http_profile = HttpProfile()
            domain = profile.get("domain", "")
            scheme = profile.get("scheme", "https")
            method = profile.get("method", "POST")
            
            http_profile.rootDomain = domain
            http_profile.scheme = scheme
            http_profile.reqMethod = method
            
            debug(f"HTTP configuration: domain={domain}, scheme={scheme}, method={method}")
            
            # Create client configuration
            client_profile = ClientProfile()
            client_profile.httpProfile = http_profile
            
            # Instantiate common client
            common_client = CommonClient(
                self._service, 
                self._api_version, 
                cred, 
                region, 
                profile=client_profile
            )
            
            debug("Tencent Cloud client created, starting API call")
            
            # Call API
            resp = common_client.call_json("GetWsToken", params)
            debug("Tencent Cloud API call successful")
            
            # Extract token
            token = ""
            if "Response" in resp and "Token" in resp["Response"]:
                token = resp["Response"]["Token"]
                debug("Successfully extracted token")
            else:
                warning("Token field not found in API response")
            
            return token
            
        except TencentCloudSDKException as err:
            error(f"Tencent Cloud SDK exception: {err}")
            return ""
        except Exception as err:
            error(f"Failed to get token: {err}")
            return ""
    
    def validate_credentials(self) -> bool:
        """
        Validate if Tencent Cloud credentials are valid
        
        Returns:
            bool: Whether credentials are valid
        """
        secret_id = self.config.get("tencent_cloud.secret_id", "")
        secret_key = self.config.get("tencent_cloud.secret_key", "")
        
        if not secret_id or not secret_key:
            print("Error: Missing Tencent Cloud credentials")
            return False
        
        return True
    
    def get_default_region(self) -> str:
        """
        Get default region
        
        Returns:
            str: Default region
        """
        return self.config.get("tencent_cloud.region", "ap-beijing")
    
    def get_service_info(self) -> Dict[str, str]:
        """
        Get service information
        
        Returns:
            Dict[str, str]: Service information
        """
        return {
            "service": self._service,
            "api_version": self._api_version,
            "region": self.get_default_region()
        } 