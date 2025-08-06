"""
生成核心模块

负责将项目内容生成多种语言。
"""

import os
import json
import re
from pathlib import Path
from typing import Dict, List, Optional, Any
from ..services.tencent_cloud import TencentCloudService
from ..services.sse_client import SSEClient
from ..utils.config import Config
from ..utils.file_utils import FileUtils
from ..models.types import TranslationRequest, TranslationResponse
from ..utils.logger import debug, info, warning, error


class Translator:
    """生成器类，负责项目内容的生成"""
    
    def __init__(self, config: Optional[Config] = None):
        """
        初始化翻译器
        
        Args:
            config: 配置对象，如果为None则使用默认配置
        """
        self.config = config or Config()
        self.tencent_service = TencentCloudService(self.config)
        self.sse_client = SSEClient(self.config)
        self.file_utils = FileUtils()
        
    def translate_project(self, project_path: str, languages: Optional[List[str]] = None) -> TranslationResponse:
        """
        生成整个项目
        
        Args:
            project_path: 项目路径
            languages: 要生成的语言列表，如果为None则使用默认语言
            
        Returns:
            TranslationResponse: 生成响应对象
        """
        # 读取项目内容
        project_content = self._read_project_content(project_path)
        
        # 检查内容长度，如果过长则分批处理
        max_content_length = 15000  # 15KB限制
        
        if len(project_content) > max_content_length:
            warning(f"⚠ 内容过长 ({len(project_content)} 字符)，将分批处理")
            return self._translate_project_in_batches(project_content, languages, max_content_length)
        else:
            # 构建生成请求
            request = self._build_translation_request(project_content, languages)
            
            # 执行生成
            response = self._execute_translation(request)
            
            return response
    
    def _read_project_content(self, project_path: str) -> str:
        """
        读取项目文件内容，支持 .gitignore 过滤和智能压缩
        
        Args:
            project_path: 项目路径
            
        Returns:
            str: 项目内容字符串
        """
        content = ""
        project_path = Path(project_path)
        
        # 检查是否存在 .gitignore 文件
        gitignore_path = project_path / ".gitignore"
        if gitignore_path.exists():
            debug(f"✓ 发现 .gitignore 文件，将过滤忽略的文件")
        else:
            warning(f"⚠ 未发现 .gitignore 文件，将读取所有文本文件")
        
        # 获取项目文件列表（应用 .gitignore 过滤）
        project_files = self.file_utils.get_project_files(project_path, include_gitignore=True)
        
        # 优先读取 README.md
        readme_files = [f for f in project_files if f.name.lower() == "readme.md"]
        if readme_files:
            readme_path = readme_files[0]
            try:
                readme_content = readme_path.read_text(encoding="utf-8")
                # 压缩README内容，保留重要部分
                compressed_readme = self._compress_content(readme_content, max_length=3000)
                content += "=== README.md ===\n"
                content += compressed_readme
                content += "\n\n"
                debug(f"✓ 已读取并压缩 {readme_path.relative_to(project_path)} ({len(compressed_readme)} 字符)")
            except Exception as e:
                error(f"✗ 读取 README.md 失败: {e}")
        else:
            warning(f"⚠ 未找到 README.md")
        
        # 智能选择最重要的文件
        other_files = [f for f in project_files if f.name.lower() != "readme.md"]
        important_files = self._select_important_files(other_files, max_files=2)
        
        if important_files:
            debug(f"✓ 从 {len(other_files)} 个文件中选择了 {len(important_files)} 个重要文件")
            
            for file_path in important_files:
                try:
                    relative_path = file_path.relative_to(project_path)
                    file_content = file_path.read_text(encoding="utf-8")
                    
                    # 智能压缩文件内容
                    compressed_content = self._compress_content(file_content, max_length=1500)
                    
                    content += f"=== {relative_path} ===\n"
                    content += compressed_content
                    content += "\n\n"
                    debug(f"✓ 已读取并压缩 {relative_path} ({len(compressed_content)} 字符)")
                except Exception as e:
                    error(f"✗ 读取 {file_path} 失败: {e}")
        else:
            warning(f"⚠ 未找到其他可读取的文件")
        
        return content
    
    def _select_important_files(self, files: List[Path], max_files: int = 2) -> List[Path]:
        """
        智能选择最重要的文件
        
        Args:
            files: 文件列表
            max_files: 最大文件数量
            
        Returns:
            List[Path]: 重要文件列表
        """
        if not files:
            return []
        
        # 定义文件重要性评分规则
        importance_scores = {}
        
        for file_path in files:
            score = 0
            file_name = file_path.name.lower()
            relative_path = str(file_path.relative_to(file_path.parents[-2] if len(file_path.parts) > 2 else file_path.parent))
            
            # 核心文件得分最高
            if any(keyword in file_name for keyword in ['main', 'core', 'translator', 'generator', 'parser']):
                score += 100
            
            # 配置文件得分较高
            if any(keyword in file_name for keyword in ['config', 'settings', 'setup']):
                score += 80
            
            # 工具类文件得分中等
            if any(keyword in file_name for keyword in ['utils', 'helpers', 'tools']):
                score += 60
            
            # 模型文件得分中等
            if any(keyword in file_name for keyword in ['models', 'types', 'schema']):
                score += 50
            
            # 服务文件得分中等
            if any(keyword in file_name for keyword in ['services', 'api', 'client']):
                score += 40
            
            # CLI文件得分较低
            if any(keyword in file_name for keyword in ['cli', 'commands']):
                score += 30
            
            # 测试文件得分最低
            if any(keyword in file_name for keyword in ['test', 'spec']):
                score += 10
            
            # 路径深度影响得分（越浅越好）
            depth_penalty = len(file_path.parts) * 5
            score -= depth_penalty
            
            importance_scores[file_path] = score
        
        # 按得分排序并返回前N个文件
        sorted_files = sorted(files, key=lambda f: importance_scores[f], reverse=True)
        return sorted_files[:max_files]
    
    def _compress_content(self, content: str, max_length: int = 2000) -> str:
        """
        智能压缩内容，保留重要部分
        
        Args:
            content: 原始内容
            max_length: 最大长度
            
        Returns:
            str: 压缩后的内容
        """
        if len(content) <= max_length:
            return content
        
        # 移除多余的空白行
        lines = content.split('\n')
        compressed_lines = []
        prev_empty = False
        
        for line in lines:
            is_empty = line.strip() == ''
            if is_empty and prev_empty:
                continue
            compressed_lines.append(line)
            prev_empty = is_empty
        
        content = '\n'.join(compressed_lines)
        
        if len(content) <= max_length:
            return content
        
        # 如果还是太长，保留开头和结尾的重要部分
        if len(content) > max_length:
            # 保留开头60%，结尾20%，中间20%用省略号
            start_length = int(max_length * 0.6)
            end_length = int(max_length * 0.2)
            
            start_part = content[:start_length]
            end_part = content[-end_length:]
            
            # 确保不截断单词
            if start_part and not start_part.endswith('\n'):
                last_newline = start_part.rfind('\n')
                if last_newline > start_length * 0.8:  # 如果离换行符不远，就截断到换行符
                    start_part = start_part[:last_newline]
            
            if end_part and not end_part.startswith('\n'):
                first_newline = end_part.find('\n')
                if first_newline < end_length * 0.2:  # 如果离换行符不远，就从换行符开始
                    end_part = end_part[first_newline:]
            
            content = f"{start_part}\n\n... (内容已压缩) ...\n\n{end_part}"
        
        return content
    
    def _translate_project_in_batches(self, project_content: str, languages: Optional[List[str]] = None, max_length: int = 30000) -> TranslationResponse:
        """
        分批生成项目内容
        
        Args:
            project_content: 项目内容
            languages: 目标语言列表
            max_length: 每批最大长度
            
        Returns:
            TranslationResponse: 生成响应对象
        """
        debug(f"📦 开始分批处理，总内容长度: {len(project_content)} 字符")
        
        # 将内容按文件分割
        content_parts = self._split_content_by_files(project_content)
        
        if not content_parts:
            return TranslationResponse(
                success=False,
                error="无法分割内容",
                languages=languages or []
            )
        
        debug(f"📦 内容已分割为 {len(content_parts)} 个部分")
        
        # 合并小部分，确保每批不超过限制
        batches = self._create_batches(content_parts, max_length)
        
        debug(f"📦 将分 {len(batches)} 批处理")
        
        all_responses = []
        
        for i, batch_content in enumerate(batches, 1):
            debug(f"📦 处理第 {i}/{len(batches)} 批 (长度: {len(batch_content)} 字符)")
            
            # 构建批次请求
            batch_request = self._build_batch_translation_request(batch_content, languages, i, len(batches))
            
            # 执行生成
            batch_response = self._execute_translation(batch_request)
            
            if not batch_response.success:
                error(f"❌ 第 {i} 批生成失败: {batch_response.error}")
                return batch_response
            
            all_responses.append(batch_response.content)
        
        # 合并所有响应
        combined_response = self._combine_batch_responses(all_responses, languages)
        
        return TranslationResponse(
            success=True,
            content=combined_response,
            languages=languages or [],
            raw_response="\n\n".join(all_responses)
        )
    
    def _split_content_by_files(self, content: str) -> List[str]:
        """
        按文件分割内容
        
        Args:
            content: 项目内容
            
        Returns:
            List[str]: 分割后的内容部分
        """
        parts = []
        current_part = ""
        
        lines = content.split('\n')
        
        for line in lines:
            # 检查是否是文件分隔符
            if line.startswith('===') and line.endswith('==='):
                # 保存当前部分
                if current_part.strip():
                    parts.append(current_part.strip())
                current_part = line + '\n'
            else:
                current_part += line + '\n'
        
        # 添加最后一部分
        if current_part.strip():
            parts.append(current_part.strip())
        
        return parts
    
    def _create_batches(self, content_parts: List[str], max_length: int) -> List[str]:
        """
        创建批次，确保每批不超过长度限制
        
        Args:
            content_parts: 内容部分列表
            max_length: 每批最大长度
            
        Returns:
            List[str]: 批次列表
        """
        batches = []
        current_batch = ""
        
        for part in content_parts:
            # 如果当前批次加上新部分会超过限制，且当前批次不为空，则开始新批次
            if current_batch and len(current_batch + part) > max_length:
                batches.append(current_batch.strip())
                current_batch = part
            else:
                if current_batch:
                    current_batch += "\n\n" + part
                else:
                    current_batch = part
        
        # 添加最后一批
        if current_batch.strip():
            batches.append(current_batch.strip())
        
        return batches
    
    def _build_batch_translation_request(self, content: str, languages: Optional[List[str]] = None, batch_num: int = 1, total_batches: int = 1) -> TranslationRequest:
        """
        构建批次生成请求
        
        Args:
            content: 批次内容
            languages: 目标语言列表
            batch_num: 当前批次号
            total_batches: 总批次数
            
        Returns:
            TranslationRequest: 生成请求对象
        """
        if languages is None:
            # 从配置文件获取默认语言
            config_languages = self.config.get("translation.default_languages", [])
            if config_languages:
                # 配置文件中的语言可能是语言名称，需要转换为语言代码
                languages = [self._normalize_language_code(lang) for lang in config_languages]
            else:
                # 如果没有配置，使用默认的语言代码
                languages = ["zh", "en", "ja"]
        
        # 将语言代码转换为语言名称
        language_names = [self.get_language_name(lang) for lang in languages]
        languages_str = "、".join(language_names)
        
        prompt = f"""这是项目内容的第 {batch_num}/{total_batches} 部分，请将以下项目代码和README生成多种语言的README文档，必须严格按照以下语言列表生成：{languages_str}。

项目内容（第 {batch_num}/{total_batches} 部分）：
{content}

请严格按照以下格式为每种语言生成完整的README文档，包含项目介绍、功能说明、使用方法等。必须包含所有要求的语言，不能遗漏或替换：

"""
        
        # 为每种语言添加格式说明
        for lang in languages:
            lang_name = self.get_language_name(lang)
            if lang == "ja":
                prompt += f"### 日本語\n[日本語README内容]\n\n"
            elif lang == "zh":
                prompt += f"### 中文\n[中文README内容]\n\n"
            elif lang == "en":
                prompt += f"### English\n[English README content]\n\n"
            else:
                prompt += f"### {lang_name}\n[{lang_name}README内容]\n\n"
        
        # 构建工作流输入变量
        workflow_variables = {
            "code_text": content,
            "language": languages_str
        }
        
        return TranslationRequest(
            content=prompt,
            languages=languages,
            bot_app_key=self.config.get("app.bot_app_key"),
            visitor_biz_id=self.config.get("app.visitor_biz_id"),
            additional_params={"workflow_variables": workflow_variables}
        )
    
    def _combine_batch_responses(self, responses: List[str], languages: Optional[List[str]] = None) -> str:
        """
        合并批次响应
        
        Args:
            responses: 响应列表
            languages: 语言列表
            
        Returns:
            str: 合并后的响应
        """
        if not responses:
            return ""
        
        if len(responses) == 1:
            return responses[0]
        
        # 简单合并，保留最后一个完整响应
        # 这里可以根据需要实现更复杂的合并逻辑
        print(f"📦 合并 {len(responses)} 个批次响应")
        
        # 返回最后一个响应，因为它通常是最完整的
        return responses[-1]
    
    def _build_translation_request(self, content: str, languages: Optional[List[str]] = None) -> TranslationRequest:
        """
        构建生成请求
        
        Args:
            content: 要生成的内容
            languages: 目标语言列表
            
        Returns:
            TranslationRequest: 生成请求对象
        """
        if languages is None:
            # 从配置文件获取默认语言
            config_languages = self.config.get("translation.default_languages", [])
            if config_languages:
                # 配置文件中的语言可能是语言名称，需要转换为语言代码
                languages = [self._normalize_language_code(lang) for lang in config_languages]
            else:
                # 如果没有配置，使用默认的语言代码
                languages = ["zh", "en", "ja"]
        
        print(f"目标语言: {languages}")
        
        # 将语言代码转换为语言名称
        language_names = [self.get_language_name(lang) for lang in languages]
        
        # 构建语言列表字符串
        languages_str = "、".join(language_names)
        
        # 构建工作流输入变量
        workflow_variables = {
            "code_text": content,
            "language": languages_str
        }
        
        # 构建简洁的prompt
        prompt = f"""生成项目为{languages_str}README，格式：

项目：{content}

要求：每种语言生成完整README，包含介绍、功能、使用方法。

格式：
"""
        
        # 为每种语言添加简洁的格式说明
        for lang in languages:
            lang_name = self.get_language_name(lang)
            if lang == "ja":
                prompt += f"### 日本語\n[内容]\n\n"
            elif lang == "zh":
                prompt += f"### 中文\n[内容]\n\n"
            elif lang == "en":
                prompt += f"### English\n[内容]\n\n"
            else:
                prompt += f"### {lang_name}\n[内容]\n\n"
        
        return TranslationRequest(
            content=prompt,
            languages=languages,
            bot_app_key=self.config.get("app.bot_app_key"),
            visitor_biz_id=self.config.get("app.visitor_biz_id"),
            additional_params={"workflow_variables": workflow_variables}
        )
    
    def _execute_translation(self, request: TranslationRequest) -> TranslationResponse:
        """
        执行生成
        
        Args:
            request: 生成请求对象
            
        Returns:
            TranslationResponse: 生成响应对象
        """
        print("正在发送生成请求...")
        
        try:
            # 使用SSE客户端发送请求
            response_text = self.sse_client.send_request(request)
            
            return TranslationResponse(
                success=True,
                content=response_text,
                languages=request.languages,
                raw_response=response_text
            )
            
        except Exception as e:
            print(f"❌ 生成失败: {e}")
            return TranslationResponse(
                success=False,
                error=str(e),
                languages=request.languages
            )
    
    def get_supported_languages(self) -> List[str]:
        """
        获取支持的语言列表
        
        Returns:
            List[str]: 支持的语言列表
        """
        return [
            "zh-Hans", "zh-Hant", "en", "ja", "ko", "fr", "de", "es", "it", "pt", "pt-PT", "ru",
            "th", "vi", "hi", "ar", "tr", "pl", "nl", "sv", "da", "no", "nb", "fi", "cs", "sk", 
            "hu", "ro", "bg", "hr", "sl", "et", "lv", "lt", "mt", "el", "ca", "eu", "gl", "af", 
            "zu", "xh", "st", "sw", "yo", "ig", "ha", "am", "or", "bn", "gu", "pa", "te", "kn", 
            "ml", "ta", "si", "my", "km", "lo", "ne", "ur", "fa", "ps", "sd", "he", "yue"
        ]
    
    def _normalize_language_code(self, lang: str) -> str:
        """
        标准化语言代码，将语言名称转换为语言代码
        
        Args:
            lang: 语言代码或语言名称
            
        Returns:
            str: 标准化的语言代码
        """
        # 反向映射：语言名称 -> 语言代码
        reverse_language_map = {
            "中文": "zh-Hans",
            "繁體中文": "zh-Hant",
            "English": "en", 
            "日本語": "ja",
            "한국어": "ko",
            "Français": "fr",
            "Deutsch": "de",
            "Español": "es",
            "Italiano": "it",
            "Português": "pt",
            "Português (Portugal)": "pt-PT",
            "Русский": "ru",
            "Tiếng Việt": "vi",
            "ไทย": "th",
            "हिन्दी": "hi",
            "العربية": "ar",
            "Türkçe": "tr",
            "Polski": "pl",
            "Nederlands": "nl",
            "Svenska": "sv",
            "Dansk": "da",
            "Norsk": "no",
            "Norsk Bokmål": "nb",
            "Suomi": "fi",
            "Čeština": "cs",
            "Slovenčina": "sk",
            "Magyar": "hu",
            "Română": "ro",
            "български": "bg",
            "Hrvatski": "hr",
            "Slovenščina": "sl",
            "Eesti": "et",
            "Latviešu": "lv",
            "Lietuvių": "lt",
            "Malti": "mt",
            "Ελληνικά": "el",
            "Català": "ca",
            "Euskara": "eu",
            "Galego": "gl",
            "Afrikaans": "af",
            "IsiZulu": "zu",
            "isiXhosa": "xh",
            "Sesotho": "st",
            "Kiswahili": "sw",
            "Èdè Yorùbá": "yo",
            "Asụsụ Igbo": "ig",
            "Hausa": "ha",
            "አማርኛ": "am",
            "ଓଡ଼ିଆ": "or",
            "বাংলা": "bn",
            "ગુજરાતી": "gu",
            "ਪੰਜਾਬੀ": "pa",
            "తెలుగు": "te",
            "ಕನ್ನಡ": "kn",
            "മലയാളം": "ml",
            "தமிழ்": "ta",
            "සිංහල": "si",
            "မြန်မာဘာသာ": "my",
            "ភាសាខ្មែរ": "km",
            "ລາວ": "lo",
            "नेपाली": "ne",
            "اردو": "ur",
            "فارسی": "fa",
            "پښتو": "ps",
            "سنڌي": "sd",
            "עברית": "he",
            "粵語": "yue"
        }
        
        # 如果已经是语言代码，直接返回
        if lang in ["zh-Hans", "zh-Hant", "en", "ja", "ko", "fr", "de", "es", "it", "pt", "pt-PT", "ru", "th", "vi", "hi", "ar", "tr", "pl", "nl", "sv", "da", "no", "nb", "fi", "cs", "sk", "hu", "ro", "bg", "hr", "sl", "et", "lv", "lt", "mt", "el", "ca", "eu", "gl", "af", "zu", "xh", "st", "sw", "yo", "ig", "ha", "am", "or", "bn", "gu", "pa", "te", "kn", "ml", "ta", "si", "my", "km", "lo", "ne", "ur", "fa", "ps", "sd", "he", "yue"]:
            return lang
        
        # 如果是语言名称，转换为语言代码
        return reverse_language_map.get(lang, lang)
    
    def get_language_name(self, lang_code: str) -> str:
        """
        获取语言代码对应的语言名称
        
        Args:
            lang_code: 语言代码
            
        Returns:
            str: 语言名称
        """
        language_map = {
            "zh-Hans": "中文",
            "zh-Hant": "繁體中文",
            "en": "English", 
            "ja": "日本語",
            "ko": "한국어",
            "fr": "Français",
            "de": "Deutsch",
            "es": "Español",
            "it": "Italiano",
            "pt": "Português",
            "pt-PT": "Português (Portugal)",
            "ru": "Русский",
            "vi": "Tiếng Việt",
            "th": "ไทย",
            "hi": "हिन्दी",
            "ar": "العربية",
            "tr": "Türkçe",
            "pl": "Polski",
            "nl": "Nederlands",
            "sv": "Svenska",
            "da": "Dansk",
            "no": "Norsk",
            "nb": "Norsk Bokmål",
            "fi": "Suomi",
            "cs": "Čeština",
            "sk": "Slovenčina",
            "hu": "Magyar",
            "ro": "Română",
            "bg": "български",
            "hr": "Hrvatski",
            "sl": "Slovenščina",
            "et": "Eesti",
            "lv": "Latviešu",
            "lt": "Lietuvių",
            "mt": "Malti",
            "el": "Ελληνικά",
            "ca": "Català",
            "eu": "Euskara",
            "gl": "Galego",
            "af": "Afrikaans",
            "zu": "IsiZulu",
            "xh": "isiXhosa",
            "st": "Sesotho",
            "sw": "Kiswahili",
            "yo": "Èdè Yorùbá",
            "ig": "Asụsụ Igbo",
            "ha": "Hausa",
            "am": "አማርኛ",
            "or": "ଓଡ଼ିଆ",
            "bn": "বাংলা",
            "gu": "ગુજરાતી",
            "pa": "ਪੰਜਾਬੀ",
            "te": "తెలుగు",
            "kn": "ಕನ್ನಡ",
            "ml": "മലയാളം",
            "ta": "தமிழ்",
            "si": "සිංහල",
            "my": "မြန်မာဘာသာ",
            "km": "ភាសាខ្មែរ",
            "lo": "ລາວ",
            "ne": "नेपाली",
            "ur": "اردو",
            "fa": "فارسی",
            "ps": "پښتو",
            "sd": "سنڌي",
            "he": "עברית",
            "yue": "粵語"
        }
        return language_map.get(lang_code, lang_code) 