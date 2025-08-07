"""
Generation core module

Responsible for generating project content in multiple languages.
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
    """Generator class, responsible for project content generation"""
    
    def __init__(self, config: Optional[Config] = None):
        """
        Initialize translator
        
        Args:
            config: Configuration object, if None then use default configuration
        """
        self.config = config or Config()
        self.tencent_service = TencentCloudService(self.config)
        self.sse_client = SSEClient(self.config)
        self.file_utils = FileUtils()
        
    def translate_project(self, project_path: str, languages: Optional[List[str]] = None) -> TranslationResponse:
        """
        Generate entire project
        
        Args:
            project_path: Project path
            languages: List of languages to generate, if None then use default languages
            
        Returns:
            TranslationResponse: Generation response object
        """
        # Read project content
        project_content = self._read_project_content(project_path)
        
        # Check content length, if too long then process in batches
        max_content_length = 15000  # 15KB limit
        
        if len(project_content) > max_content_length:
            warning(f"⚠ Content too long ({len(project_content)} characters), will process in batches")
            return self._translate_project_in_batches(project_content, languages, max_content_length)
        else:
            # Build generation request
            request = self._build_translation_request(project_content, languages)
            
            # Execute generation
            response = self._execute_translation(request)
            
            return response
    
    def translate_text_only(self, text: str, languages: Optional[List[str]] = None) -> TranslationResponse:
        """
        Pure text translation function
        
        Args:
            text: Text content to translate
            languages: Target language list
            
        Returns:
            TranslationResponse: Translation response object
        """
        # Build pure translation request
        request = self._build_text_translation_request(text, languages)
        
        # Execute translation
        response = self._execute_translation(request)
        
        return response
    
    def _read_project_content(self, project_path: str) -> str:
        """
        Read project file content, supports .gitignore filtering and intelligent compression
        
        Args:
            project_path: Project path
            
        Returns:
            str: Project content string
        """
        content = ""
        project_path = Path(project_path)
        
        # Check if .gitignore file exists
        gitignore_path = project_path / ".gitignore"
        if gitignore_path.exists():
            debug(f"✓ Found .gitignore file, will filter ignored files")
        else:
            warning(f"⚠ No .gitignore file found, will read all text files")
        
        # Get project file list (apply .gitignore filtering)
        project_files = self.file_utils.get_project_files(project_path, include_gitignore=True)
        
        # Prioritize reading README.md
        readme_files = [f for f in project_files if f.name.lower() == "readme.md"]
        if readme_files:
            readme_path = readme_files[0]
            try:
                readme_content = readme_path.read_text(encoding="utf-8")
                # Compress README content, keep important parts
                compressed_readme = self._compress_content(readme_content, max_length=3000)
                content += "=== README.md ===\n"
                content += compressed_readme
                content += "\n\n"
                debug(f"✓ Read and compressed {readme_path.relative_to(project_path)} ({len(compressed_readme)} characters)")
            except Exception as e:
                error(f"✗ Failed to read README.md: {e}")
        else:
            warning(f"⚠ README.md not found")
        
        # Intelligently select the most important files
        other_files = [f for f in project_files if f.name.lower() != "readme.md"]
        important_files = self._select_important_files(other_files, max_files=2)
        
        if important_files:
            debug(f"✓ Selected {len(important_files)} important files from {len(other_files)} files")
            
            for file_path in important_files:
                try:
                    relative_path = file_path.relative_to(project_path)
                    file_content = file_path.read_text(encoding="utf-8")
                    
                    # Intelligently compress file content
                    compressed_content = self._compress_content(file_content, max_length=1500)
                    
                    content += f"=== {relative_path} ===\n"
                    content += compressed_content
                    content += "\n\n"
                    debug(f"✓ Read and compressed {relative_path} ({len(compressed_content)} characters)")
                except Exception as e:
                    error(f"✗ Failed to read {file_path}: {e}")
        else:
            warning(f"⚠ No other readable files found")
        
        return content
    
    def _read_readme_file(self, project_path: str) -> str:
        """
        Read README file in project root directory
        
        Args:
            project_path: Project path
            
        Returns:
            str: README file content, returns empty string if read fails
        """
        try:
            project_path = Path(project_path)
            readme_files = [
                project_path / "README.md",
                project_path / "readme.md",
                project_path / "README.txt",
                project_path / "readme.txt"
            ]
            
            for readme_file in readme_files:
                if readme_file.exists():
                    content = readme_file.read_text(encoding="utf-8")
                    debug(f"Successfully read README file: {readme_file}")
                    
                    # Remove the first line if it starts with > (language note)
                    content = self._remove_language_note_from_content(content)
                    
                    return content
            
            # If no README file found, return empty string
            debug(f"No README file found in project path {project_path}")
            return ""
            
        except Exception as e:
            error(f"Failed to read README file: {e}")
            return ""
    
    def _select_important_files(self, files: List[Path], max_files: int = 2) -> List[Path]:
        """
        Intelligently select the most important files
        
        Args:
            files: File list
            max_files: Maximum number of files
            
        Returns:
            List[Path]: List of important files
        """
        if not files:
            return []
        
        # Define file importance scoring rules
        importance_scores = {}
        
        for file_path in files:
            score = 0
            file_name = file_path.name.lower()
            relative_path = str(file_path.relative_to(file_path.parents[-2] if len(file_path.parts) > 2 else file_path.parent))
            
            # Core files get highest score
            if any(keyword in file_name for keyword in ['main', 'core', 'translator', 'generator', 'parser']):
                score += 100
            
            # Configuration files get higher score
            if any(keyword in file_name for keyword in ['config', 'settings', 'setup']):
                score += 80
            
            # Utility files get medium score
            if any(keyword in file_name for keyword in ['utils', 'helpers', 'tools']):
                score += 60
            
            # Model files get medium score
            if any(keyword in file_name for keyword in ['models', 'types', 'schema']):
                score += 50
            
            # Service files get medium score
            if any(keyword in file_name for keyword in ['services', 'api', 'client']):
                score += 40
            
            # CLI files get lower score
            if any(keyword in file_name for keyword in ['cli', 'commands']):
                score += 30
            
            # Test files get lowest score
            if any(keyword in file_name for keyword in ['test', 'spec']):
                score += 10
            
            # Path depth affects score (shallower is better)
            depth_penalty = len(file_path.parts) * 5
            score -= depth_penalty
            
            importance_scores[file_path] = score
        
        # Sort by score and return top N files
        sorted_files = sorted(files, key=lambda f: importance_scores[f], reverse=True)
        return sorted_files[:max_files]
    
    def _compress_content(self, content: str, max_length: int = 2000) -> str:
        """
        Intelligently compress content, keep important parts
        
        Args:
            content: Original content
            max_length: Maximum length
            
        Returns:
            str: Compressed content
        """
        if len(content) <= max_length:
            return content
        
        # Remove excessive blank lines
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
        
        # If still too long, keep important parts from beginning and end
        if len(content) > max_length:
            # Keep 60% from beginning, 20% from end, 20% in middle with ellipsis
            start_length = int(max_length * 0.6)
            end_length = int(max_length * 0.2)
            
            start_part = content[:start_length]
            end_part = content[-end_length:]
            
            # Ensure not to truncate words
            if start_part and not start_part.endswith('\n'):
                last_newline = start_part.rfind('\n')
                if last_newline > start_length * 0.8:  # If not far from newline, truncate to newline
                    start_part = start_part[:last_newline]
            
            if end_part and not end_part.startswith('\n'):
                first_newline = end_part.find('\n')
                if first_newline < end_length * 0.2:  # If not far from newline, start from newline
                    end_part = end_part[first_newline:]
            
            content = f"{start_part}\n\n... (content compressed) ...\n\n{end_part}"
        
        return content
    
    def _translate_project_in_batches(self, project_content: str, languages: Optional[List[str]] = None, max_length: int = 30000) -> TranslationResponse:
        """
        Generate project content in batches
        
        Args:
            project_content: Project content
            languages: Target language list
            max_length: Maximum length per batch
            
        Returns:
            TranslationResponse: Generation response object
        """
        debug(f"📦 Starting batch processing, total content length: {len(project_content)} characters")
        
        # Split content by files
        content_parts = self._split_content_by_files(project_content)
        
        if not content_parts:
            return TranslationResponse(
                success=False,
                error="Unable to split content",
                languages=languages or []
            )
        
        debug(f"📦 Content split into {len(content_parts)} parts")
        
        # Merge small parts, ensure each batch doesn't exceed limit
        batches = self._create_batches(content_parts, max_length)
        
        debug(f"📦 Will process in {len(batches)} batches")
        
        all_responses = []
        
        for i, batch_content in enumerate(batches, 1):
            debug(f"📦 Processing batch {i}/{len(batches)} (length: {len(batch_content)} characters)")
            
            # Build batch request
            batch_request = self._build_batch_translation_request(batch_content, languages, i, len(batches))
            
            # Execute generation
            batch_response = self._execute_translation(batch_request)
            
            if not batch_response.success:
                error(f"❌ Batch {i} generation failed: {batch_response.error}")
                return batch_response
            
            all_responses.append(batch_response.content)
        
        # Merge all responses
        combined_response = self._combine_batch_responses(all_responses, languages)
        
        return TranslationResponse(
            success=True,
            content=combined_response,
            languages=languages or [],
            raw_response="\n\n".join(all_responses)
        )
    
    def _split_content_by_files(self, content: str) -> List[str]:
        """
        Split content by files
        
        Args:
            content: Project content
            
        Returns:
            List[str]: Split content parts
        """
        parts = []
        current_part = ""
        
        lines = content.split('\n')
        
        for line in lines:
            # Check if it's a file separator
            if line.startswith('===') and line.endswith('==='):
                # Save current part
                if current_part.strip():
                    parts.append(current_part.strip())
                current_part = line + '\n'
            else:
                current_part += line + '\n'
        
        # Add last part
        if current_part.strip():
            parts.append(current_part.strip())
        
        return parts
    
    def _create_batches(self, content_parts: List[str], max_length: int) -> List[str]:
        """
        Create batches, ensure each batch doesn't exceed length limit
        
        Args:
            content_parts: Content parts list
            max_length: Maximum length per batch
            
        Returns:
            List[str]: Batch list
        """
        batches = []
        current_batch = ""
        
        for part in content_parts:
            # If current batch plus new part would exceed limit, and current batch is not empty, start new batch
            if current_batch and len(current_batch + part) > max_length:
                batches.append(current_batch.strip())
                current_batch = part
            else:
                if current_batch:
                    current_batch += "\n\n" + part
                else:
                    current_batch = part
        
        # Add last batch
        if current_batch.strip():
            batches.append(current_batch.strip())
        
        return batches
    
    def _build_batch_translation_request(self, content: str, languages: Optional[List[str]] = None, batch_num: int = 1, total_batches: int = 1) -> TranslationRequest:
        """
        Build batch generation request
        
        Args:
            content: Batch content
            languages: Target language list
            batch_num: Current batch number
            total_batches: Total number of batches
            
        Returns:
            TranslationRequest: Generation request object
        """
        if languages is None:
            # Get default languages from configuration
            config_languages = self.config.get("translation.default_languages", [])
            if config_languages:
                # Languages in configuration might be language names, need to convert to language codes
                languages = [self._normalize_language_code(lang) for lang in config_languages]
            else:
                # If not configured, use default language codes
                languages = ["zh", "en", "ja"]
        
        # Convert language codes to language names
        language_names = [self.get_language_name(lang) for lang in languages]
        languages_str = "、".join(language_names)
        
        prompt = f"""This is part {batch_num}/{total_batches} of the project content. Please generate multi-language README documents from the following project code and README, strictly following the language list: {languages_str}.

Project content (part {batch_num}/{total_batches}):
{content}

Please strictly follow the following format to generate complete README documents for each language, including project introduction, feature description, usage instructions, etc. Must include all required languages, cannot omit or replace:

"""
        
        # Add format instructions for each language
        for lang in languages:
            lang_name = self.get_language_name(lang)
            if lang == "ja":
                prompt += f"### 日本語\n[Japanese README content]\n\n"
            elif lang == "zh":
                prompt += f"### 中文\n[Chinese README content]\n\n"
            elif lang == "en":
                prompt += f"### English\n[English README content]\n\n"
            else:
                prompt += f"### {lang_name}\n[{lang_name} README content]\n\n"
        
        # Build workflow input variables
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
        Combine batch responses
        
        Args:
            responses: Response list
            languages: Language list
            
        Returns:
            str: Combined response
        """
        if not responses:
            return ""
        
        if len(responses) == 1:
            return responses[0]
        
        # Simple merge, keep the last complete response
        # More complex merge logic can be implemented here as needed
        print(f"📦 Merging {len(responses)} batch responses")
        
        # Return the last response, as it's usually the most complete
        return responses[-1]
    
    def _build_translation_request(self, content: str, languages: Optional[List[str]] = None) -> TranslationRequest:
        """
        Build generation request
        
        Args:
            content: Content to generate
            languages: Target language list
            
        Returns:
            TranslationRequest: Generation request object
        """
        if languages is None:
            # Get default languages from configuration
            config_languages = self.config.get("translation.default_languages", [])
            if config_languages:
                # Languages in configuration might be language names, need to convert to language codes
                languages = [self._normalize_language_code(lang) for lang in config_languages]
            else:
                # If not configured, use default language codes
                languages = ["zh", "en", "ja"]
        
        print(f"Target languages: {languages}")
        
        # Convert language codes to language names
        language_names = [self.get_language_name(lang) for lang in languages]
        
        # Build language list string
        languages_str = "、".join(language_names)
        
        # Build workflow input variables
        workflow_variables = {
            "code_text": content,
            "language": languages_str
        }
        
        # Build concise prompt
        prompt = f"""Generate project as {languages_str} README, format:

Project: {content}

Requirements: Generate complete README for each language, including introduction, features, usage instructions.

Format:
"""
        
        # Add concise format instructions for each language
        for lang in languages:
            lang_name = self.get_language_name(lang)
            if lang == "ja":
                prompt += f"### 日本語\n[Content]\n\n"
            elif lang == "zh":
                prompt += f"### 中文\n[Content]\n\n"
            elif lang == "en":
                prompt += f"### English\n[Content]\n\n"
            else:
                prompt += f"### {lang_name}\n[Content]\n\n"
        
        return TranslationRequest(
            content=prompt,
            languages=languages,
            bot_app_key=self.config.get("app.bot_app_key"),
            visitor_biz_id=self.config.get("app.visitor_biz_id"),
            additional_params={"workflow_variables": workflow_variables}
        )
    
    def _execute_translation(self, request: TranslationRequest) -> TranslationResponse:
        """
        Execute generation
        
        Args:
            request: Generation request object
            
        Returns:
            TranslationResponse: Generation response object
        """
        print("Sending generation request...")
        
        try:
            # Use SSE client to send request
            response_text = self.sse_client.send_request(request)
            
            return TranslationResponse(
                success=True,
                content=response_text,
                languages=request.languages,
                raw_response=response_text
            )
            
        except Exception as e:
            print(f"❌ Generation failed: {e}")
            return TranslationResponse(
                success=False,
                error=str(e),
                languages=request.languages
            )
    
    def get_supported_languages(self) -> List[str]:
        """
        Get supported language list
        
        Returns:
            List[str]: Supported language list
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
        Normalize language code, convert language names to language codes
        
        Args:
            lang: Language code or language name
            
        Returns:
            str: Normalized language code
        """
        # Reverse mapping: language name -> language code
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
        
        # If already a language code, return directly
        if lang in ["zh-Hans", "zh-Hant", "en", "ja", "ko", "fr", "de", "es", "it", "pt", "pt-PT", "ru", "th", "vi", "hi", "ar", "tr", "pl", "nl", "sv", "da", "no", "nb", "fi", "cs", "sk", "hu", "ro", "bg", "hr", "sl", "et", "lv", "lt", "mt", "el", "ca", "eu", "gl", "af", "zu", "xh", "st", "sw", "yo", "ig", "ha", "am", "or", "bn", "gu", "pa", "te", "kn", "ml", "ta", "si", "my", "km", "lo", "ne", "ur", "fa", "ps", "sd", "he", "yue"]:
            return lang
        
        # If it's a language name, convert to language code
        return reverse_language_map.get(lang, lang)
    
    def get_language_name(self, lang_code: str) -> str:
        """
        Get language name corresponding to language code
        
        Args:
            lang_code: Language code
            
        Returns:
            str: Language name
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
    
    def _remove_language_note_from_content(self, content: str) -> str:
        """
        Remove language note from the beginning of content if it starts with >
        
        Args:
            content: Original content
            
        Returns:
            str: Content with language note removed
        """
        if not content:
            return content
        
        lines = content.split('\n')
        
        # Check if the first line starts with >
        if lines and lines[0].strip().startswith('>'):
            debug("Removing existing language note from README content")
            # Remove the first line and any following empty lines
            while lines and (lines[0].strip().startswith('>') or lines[0].strip() == ''):
                lines.pop(0)
            
            # Rejoin the content
            return '\n'.join(lines)
        
        return content 

    def _build_text_translation_request(self, text: str, languages: Optional[List[str]] = None) -> TranslationRequest:
        """
        Build pure text translation request
        
        Args:
            text: Text content to translate
            languages: Target language list
            
        Returns:
            TranslationRequest: Translation request object
        """
        if languages is None:
            # Get default languages from configuration
            config_languages = self.config.get("translation.default_languages", [])
            if config_languages:
                # Languages in configuration might be language names, need to convert to language codes
                languages = [self._normalize_language_code(lang) for lang in config_languages]
            else:
                # If not configured, use default language codes
                languages = ["zh-Hans", "en", "ja"]
        
        print(f"Target languages: {languages}")
        
        # Convert language codes to language names
        language_names = [self.get_language_name(lang) for lang in languages]
        
        # Build language list string
        languages_str = "、".join(language_names)
        
        # Build workflow input variables (without code_text parameter)
        workflow_variables = {
            "language": languages_str
        }
        
        # Build concise prompt
        prompt = f"""Please translate the following text into {languages_str}, format:

Original text: {text}

Requirements: Generate complete translation for each language, maintain original format and structure.

Format:
"""
        
        # Add concise format instructions for each language
        for lang in languages:
            lang_name = self.get_language_name(lang)
            if lang == "ja":
                prompt += f"### 日本語\n[Translated content]\n\n"
            elif lang == "zh-Hans":
                prompt += f"### 中文\n[Translated content]\n\n"
            elif lang == "en":
                prompt += f"### English\n[Translated content]\n\n"
            else:
                prompt += f"### {lang_name}\n[Translated content]\n\n"
        
        return TranslationRequest(
            content=prompt,
            languages=languages,
            bot_app_key=self.config.get("app.bot_app_key"),
            visitor_biz_id=self.config.get("app.visitor_biz_id"),
            additional_params={"workflow_variables": workflow_variables}
        ) 