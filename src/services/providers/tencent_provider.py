"""
Tencent Cloud translation provider module

Provides Tencent Cloud based translation service.
"""

import json
import time
import uuid
import sseclient
import requests
from typing import List, Dict, Any, Optional

from .base import TranslationProvider
from ...utils.config import Config
from ...utils.logger import debug, info, warning, error


class TencentProvider(TranslationProvider):
    """Tencent Cloud translation provider"""
    
    SSE_URL = "https://wss.lke.cloud.tencent.com/v1/qbot/chat/sse"
    
    def __init__(self, config: Config):
        """
        Initialize Tencent provider
        
        Args:
            config: Configuration object
        """
        self.config = config
        self.streaming_throttle = config.get("sse.streaming_throttle", 1)
        self.timeout = config.get("sse.timeout", 60)
        debug("Tencent provider initialized")
    
    @property
    def name(self) -> str:
        return "tencent"
    
    def translate(self, content: str, languages: List[str], **kwargs) -> str:
        """
        Execute translation using Tencent Cloud
        
        Args:
            content: Content to translate
            languages: Target language list
            **kwargs: Additional parameters (mode, workflow_variables, etc.)
            
        Returns:
            str: Translated content
        """
        mode = kwargs.get("mode", "gen")
        prompt = self.build_translation_prompt(content, languages, mode)
        
        language_names = [self.get_language_name(lang) for lang in languages]
        languages_str = "、".join(language_names)
        
        workflow_variables = kwargs.get("workflow_variables", {
            "code_text": content,
            "language": languages_str
        })
        
        req_data = {
            "content": prompt,
            "bot_app_key": self.config.get("app.bot_app_key"),
            "visitor_biz_id": self.config.get("app.visitor_biz_id", "duoreadme-user"),
            "workflow_variables": workflow_variables
        }
        
        return self._send_sse_request(req_data)
    
    def validate_credentials(self) -> bool:
        """
        Validate if Tencent Cloud credentials are valid
        
        Returns:
            bool: Whether credentials are valid
        """
        bot_app_key = self.config.get("app.bot_app_key", "")
        secret_id = self.config.get("tencent_cloud.secret_id", "")
        secret_key = self.config.get("tencent_cloud.secret_key", "")
        
        if not bot_app_key:
            error("Missing bot_app_key")
            return False
        
        if not secret_id or not secret_key:
            warning("Missing Tencent Cloud secret_id or secret_key")
        
        return True
    
    def _send_sse_request(self, req_data: Dict[str, Any]) -> str:
        """
        Send SSE request to Tencent Cloud
        
        Args:
            req_data: Request data
            
        Returns:
            str: Response content
        """
        session_id = str(uuid.uuid4())
        
        request_data = {
            "content": req_data["content"],
            "bot_app_key": req_data["bot_app_key"],
            "visitor_biz_id": req_data["visitor_biz_id"],
            "session_id": session_id,
            "streaming_throttle": self.streaming_throttle
        }
        
        if "workflow_variables" in req_data:
            request_data["custom_variables"] = req_data["workflow_variables"]
        
        headers = {"Accept": "text/event-stream"}
        
        try:
            debug(f"Sending request to: {self.SSE_URL}")
            debug(f"Request data: {json.dumps(request_data, ensure_ascii=False, indent=2)}")
            
            response = requests.post(
                self.SSE_URL, 
                data=json.dumps(request_data),
                stream=True,
                headers=headers,
                timeout=self.timeout
            )
            
            debug(f"Response status code: {response.status_code}")
            
            if response.status_code != 200:
                error(f"Response content: {response.text}")
                raise Exception(f"HTTP request failed: {response.status_code} - {response.text}")
            
            client = sseclient.SSEClient(response)
            response_text = ""
            
            debug("Starting to process SSE response...")
            
            for event in client.events():
                debug(f"Received event: {event.event}")
                debug(f"Event data: {event.data}")
                
                try:
                    data = json.loads(event.data)
                    if event.event == "reply":
                        if data["payload"]["is_from_self"]:
                            debug(f'Sent content: {data["payload"]["content"]}')
                        elif data["payload"]["is_final"]:
                            info(f"Received event: {event.event}")
                            debug(f"Event data: {event.data}")
                            info("Polishing completed")
                            response_text = data["payload"]["content"]
                            break
                        else:
                            content = data["payload"]["content"]
                            response_text += content
                            
                            if self.streaming_throttle > 0:
                                time.sleep(self.streaming_throttle / 1000.0)
                    else:
                        debug(f"Unhandled event type: {event.event}")
                
                except json.JSONDecodeError as e:
                    error(f"JSON parsing failed: {e}")
                    continue
                except Exception as e:
                    error(f"Failed to process SSE event: {e}")
                    continue
            
            debug(f"Final response text length: {len(response_text)}")
            info(f"Final response text length: {len(response_text)}")
            return response_text
            
        except requests.exceptions.Timeout:
            raise Exception("Request timeout")
        except requests.exceptions.RequestException as e:
            raise Exception(f"Network request failed: {e}")
        except Exception as e:
            raise Exception(f"SSE request failed: {e}")
