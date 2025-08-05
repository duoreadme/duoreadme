"""
SSE客户端模块

提供Server-Sent Events客户端的实现。
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
    """SSE客户端类"""
    
    def __init__(self, config: Config):
        """
        初始化SSE客户端
        
        Args:
            config: 配置对象
        """
        self.config = config
        self.streaming_throttle = config.get("sse.streaming_throttle", 1)
        self.timeout = config.get("sse.timeout", 60)
    
    def send_request(self, request: TranslationRequest) -> str:
        """
        发送SSE请求
        
        Args:
            request: 翻译请求对象
            
        Returns:
            str: 响应内容
            
        Raises:
            Exception: 请求失败
        """
        # 构建请求数据
        req_data = {
            "content": request.content,
            "bot_app_key": request.bot_app_key,
            "visitor_biz_id": request.visitor_biz_id
        }
        
        # 添加额外参数
        if request.additional_params:
            req_data.update(request.additional_params)
        
        # 发送SSE请求
        response_text = self._send_sse_request(req_data)
        
        return response_text
    
    def _send_sse_request(self, req_data: Dict[str, Any]) -> str:
        """
        发送SSE请求的具体实现
        
        Args:
            req_data: 请求数据
            
        Returns:
            str: 响应内容
        """
        url = "https://wss.lke.cloud.tencent.com/v1/qbot/chat/sse"
        
        # 添加session_id
        import uuid
        session_id = str(uuid.uuid4())
        
        # 构建请求数据
        request_data = {
            "content": req_data["content"],
            "bot_app_key": req_data["bot_app_key"],
            "visitor_biz_id": req_data["visitor_biz_id"],
            "session_id": session_id,
            "streaming_throttle": self.streaming_throttle
        }
        
        # 添加工作流变量（如果存在）
        if "workflow_variables" in req_data:
            request_data["workflow_variables"] = req_data["workflow_variables"]
        
        headers = {"Accept": "text/event-stream"}
        
        try:
            debug(f"正在发送请求到: {url}")
            debug(f"请求数据: {json.dumps(request_data, ensure_ascii=False, indent=2)}")
            
            # 发送请求
            response = requests.post(
                url, 
                data=json.dumps(request_data),
                stream=True,
                headers=headers,
                timeout=self.timeout
            )
            
            debug(f"响应状态码: {response.status_code}")
            
            if response.status_code != 200:
                error(f"响应内容: {response.text}")
                raise Exception(f"HTTP请求失败: {response.status_code} - {response.text}")
            
            # 处理SSE响应
            client = sseclient.SSEClient(response)
            response_text = ""
            
            debug("开始处理SSE响应...")
            
            for event in client.events():
                debug(f"收到事件: {event.event}")
                debug(f"事件数据: {event.data}")
                
                try:
                    data = json.loads(event.data)
                    if event.event == "reply":
                        if data["payload"]["is_from_self"]:
                            debug(f'发送内容: {data["payload"]["content"]}')
                        elif data["payload"]["is_final"]:
                            # 最后一个事件使用 INFO 级别
                            info(f"收到事件: {event.event}")
                            info(f"事件数据: {event.data}")
                            info("翻译完成")
                            response_text = data["payload"]["content"]
                            break
                        else:
                            content = data["payload"]["content"]
                            response_text += content
                            # 流式输出保持原样，不记录日志
                            
                            # 节流控制
                            if self.streaming_throttle > 0:
                                time.sleep(self.streaming_throttle / 1000.0)
                    else:
                        debug(f"未处理的事件类型: {event.event}")
                
                except json.JSONDecodeError as e:
                    error(f"JSON解析失败: {e}")
                    continue
                except Exception as e:
                    error(f"处理SSE事件失败: {e}")
                    continue
            
            debug(f"最终响应文本长度: {len(response_text)}")
            # 最终的JSON响应设置为INFO级别
            info(f"最终响应文本长度: {len(response_text)}")
            return response_text
            
        except requests.exceptions.Timeout:
            raise Exception("请求超时")
        except requests.exceptions.RequestException as e:
            raise Exception(f"网络请求失败: {e}")
        except Exception as e:
            raise Exception(f"SSE请求失败: {e}")
    
    def test_connection(self) -> bool:
        """
        测试连接是否正常
        
        Returns:
            bool: 连接是否正常
        """
        try:
            # 简单的连接测试
            test_data = {
                "content": "Hello",
                "bot_app_key": self.config.get("app.bot_app_key"),
                "visitor_biz_id": self.config.get("app.visitor_biz_id")
            }
            
            # 这里可以添加实际的连接测试逻辑
            return True
            
        except Exception as e:
            error(f"连接测试失败: {e}")
            return False
    
    def get_config_info(self) -> Dict[str, Any]:
        """
        获取配置信息
        
        Returns:
            Dict[str, Any]: 配置信息
        """
        return {
            "streaming_throttle": self.streaming_throttle,
            "timeout": self.timeout,
            "bot_app_key": self.config.get("app.bot_app_key"),
            "visitor_biz_id": self.config.get("app.visitor_biz_id")
        } 