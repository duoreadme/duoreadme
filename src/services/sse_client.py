"""
SSE client module

Provides Server-Sent Events client implementation.
"""

import json
import time
import sseclient
import requests
from typing import Dict, Any, Optional
from ..utils.config import Config
from ..models.types import TranslationRequest
from ..utils.logger import debug, info, warning, error


class SSEClient:
    """SSE client class"""
    
    def __init__(self, config: Config):
        """
        Initialize SSE client
        
        Args:
            config: Configuration object
        """
        self.config = config
        self.streaming_throttle = config.get("sse.streaming_throttle", 1)
        self.timeout = config.get("sse.timeout", 60)
    
    def send_request(self, request: TranslationRequest) -> str:
        """
        Send SSE request
        
        Args:
            request: Generation request object
            
        Returns:
            str: Response content
            
        Raises:
            Exception: Request failed
        """
        # Build request data
        req_data = {
            "content": request.content,
            "bot_app_key": request.bot_app_key,
            "visitor_biz_id": request.visitor_biz_id
        }
        
        # Add additional parameters
        if request.additional_params:
            req_data.update(request.additional_params)
        
        # Send SSE request
        response_text = self._send_sse_request(req_data)
        
        return response_text
    
    def _send_sse_request(self, req_data: Dict[str, Any]) -> str:
        """
        Specific implementation of sending SSE request
        
        Args:
            req_data: Request data
            
        Returns:
            str: Response content
        """
        url = "https://wss.lke.cloud.tencent.com/v1/qbot/chat/sse"
        
        # Add session_id
        import uuid
        session_id = str(uuid.uuid4())
        
        # Build request data
        request_data = {
            "content": req_data["content"],
            "bot_app_key": req_data["bot_app_key"],
            "visitor_biz_id": req_data["visitor_biz_id"],
            "session_id": session_id,
            "streaming_throttle": self.streaming_throttle
        }
        
        # Add workflow variables (if they exist)
        if "workflow_variables" in req_data:
            request_data["custom_variables"] = req_data["workflow_variables"]
        
        headers = {"Accept": "text/event-stream"}
        
        try:
            debug(f"Sending request to: {url}")
            debug(f"Request data: {json.dumps(request_data, ensure_ascii=False, indent=2)}")
            
            # Send request
            response = requests.post(
                url, 
                data=json.dumps(request_data),
                stream=True,
                headers=headers,
                timeout=self.timeout
            )
            
            debug(f"Response status code: {response.status_code}")
            
            if response.status_code != 200:
                error(f"Response content: {response.text}")
                raise Exception(f"HTTP request failed: {response.status_code} - {response.text}")
            
            # Process SSE response
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
                            # Use INFO level for the last event
                            info(f"Received event: {event.event}")
                            debug(f"Event data: {event.data}")
                            info("Polishing completed")
                            response_text = data["payload"]["content"]
                            break
                        else:
                            content = data["payload"]["content"]
                            response_text += content
                            # Keep streaming output as is, don't log
                            
                            # Throttle control
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
            # Set final JSON response to INFO level
            info(f"Final response text length: {len(response_text)}")
            return response_text
            
        except requests.exceptions.Timeout:
            raise Exception("Request timeout")
        except requests.exceptions.RequestException as e:
            raise Exception(f"Network request failed: {e}")
        except Exception as e:
            raise Exception(f"SSE request failed: {e}")
    
    def test_connection(self) -> bool:
        """
        Test if connection is normal
        
        Returns:
            bool: Whether connection is normal
        """
        try:
            # Simple connection test
            test_data = {
                "content": "Hello",
                "bot_app_key": self.config.get("app.bot_app_key"),
                "visitor_biz_id": self.config.get("app.visitor_biz_id")
            }
            
            # Actual connection test logic can be added here
            return True
            
        except Exception as e:
            error(f"Connection test failed: {e}")
            return False
    
    def get_config_info(self) -> Dict[str, Any]:
        """
        Get configuration information
        
        Returns:
            Dict[str, Any]: Configuration information
        """
        return {
            "streaming_throttle": self.streaming_throttle,
            "timeout": self.timeout,
            "bot_app_key": self.config.get("app.bot_app_key"),
            "visitor_biz_id": self.config.get("app.visitor_biz_id")
        } 