"""
SiliconFlow translation provider module

Provides SiliconFlow API based translation service with async parallel requests.
"""

import json
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict, Any, Optional, Tuple

from .base import TranslationProvider
from ...utils.config import Config
from ...utils.logger import debug, info, warning, error


class SiliconFlowProvider(TranslationProvider):
    """SiliconFlow API translation provider with async parallel requests"""
    
    API_URL = "https://api.siliconflow.cn/v1/chat/completions"
    
    def __init__(self, config: Config):
        """
        Initialize SiliconFlow provider
        
        Args:
            config: Configuration object
        """
        self.config = config
        self.api_key = config.get("siliconflow.api_key", "")
        self.model = config.get("siliconflow.model", "deepseek-ai/DeepSeek-R1-0528-Qwen3-8B")
        self.timeout = config.get("siliconflow.timeout", 120)
        self.max_tokens = config.get("siliconflow.max_tokens", 4096)
        self.temperature = config.get("siliconflow.temperature", 0.1)
        self.top_p = config.get("siliconflow.top_p", 0.7)
        self.top_k = config.get("siliconflow.top_k", 50)
        self.frequency_penalty = config.get("siliconflow.frequency_penalty", 1.0)
        self.max_workers = config.get("siliconflow.max_workers", 3)
        debug(f"SiliconFlow provider initialized with model: {self.model}")
    
    @property
    def name(self) -> str:
        return "siliconflow"
    
    def _build_single_language_prompt(self, content: str, language: str, mode: str = "gen") -> str:
        """
        Build translation prompt for a single language
        
        Args:
            content: Content to translate
            language: Target language code
            mode: Translation mode ("gen" or "trans")
            
        Returns:
            str: Translation prompt
        """
        language_name = self.get_language_name(language)
        
        if mode == "trans":
            prompt = f"""
CRITICAL RULES - VIOLATION WILL CAUSE FAILURE:
- Output ONLY the translated document. Nothing else.
- Do NOT add language headers like "### 中文" or "### English".
- Do NOT add notes, comments, or explanations like "(Note: ...)".
- Do NOT wrap in ```markdown``` code blocks.
- Do NOT translate code blocks or inline code.
- Keep exact Markdown formatting, HTML tags, links, symbols.
- Start directly with the first line of the translated document.

Now Translate this Markdown document into {language_name}:

{content}
"""
        else:
            prompt = f"""Write a README document in {language_name} ONLY for this project.

PROJECT INFO:
{content}

STRICT RULES:
1. Output ONLY in {language_name}. No other languages.
2. Keep proper Markdown formatting.
3. Include: introduction, features, installation, usage.
4. Do NOT add any explanations or notes.
5. Start directly with the README content."""
        
        return prompt
    
    def _clean_translation_output(self, content: str) -> str:
        """
        Clean up unwanted patterns from translation output
        """
        import re
        
        # Remove prompt contamination patterns at the beginning
        content = re.sub(r'^Please translate.*?(?:format|日本語)[:\s]*\n*', '', content, flags=re.IGNORECASE | re.DOTALL)
        content = re.sub(r'^Original text:\s*', '', content, flags=re.IGNORECASE)
        content = re.sub(r'^Translate.*?:\s*\n*', '', content, flags=re.IGNORECASE)
        
        lines = content.split('\n')
        cleaned_lines = []
        skip_until_content = True
        
        for line in lines:
            # Skip language headers at the beginning
            if skip_until_content:
                if re.match(r'^#{1,3}\s*(中文|English|日本語|简体中文|繁體中文|Japanese|Chinese)', line, re.IGNORECASE):
                    continue
                if line.strip() == '':
                    continue
                if line.strip() in ('```markdown', '```'):
                    continue
                skip_until_content = False
            
            # Clean repetition patterns within a line (e.g., "debug debug debug debug")
            cleaned_line = self._remove_repetitions(line)
            cleaned_lines.append(cleaned_line)
        
        result = '\n'.join(cleaned_lines)
        
        # Remove trailing ```
        result = re.sub(r'\n```\s*$', '', result)
        
        # Remove (Note: ...) patterns
        result = re.sub(r'\s*\(Note:.*?\)', '', result)
        
        # Remove repeated "Requirements:" blocks at the end
        result = re.sub(r'(Requirements:.*?structure\.)\s*\1+', r'\1', result, flags=re.DOTALL)
        
        # Remove CRITICAL RULES prompt contamination at the end
        result = re.sub(r'\n*CRITICAL RULES.*$', '', result, flags=re.DOTALL | re.IGNORECASE)
        
        # Remove any trailing prompt-like instructions
        result = re.sub(r'\n*(?:Do NOT|ONLY|Keep exact|Start directly).*$', '', result, flags=re.DOTALL)
        
        return result.strip()
    
    def _remove_repetitions(self, line: str) -> str:
        """Remove word/phrase repetitions within a line"""
        import re
        
        # Match patterns like "word word word word" (3+ repetitions)
        result = re.sub(r'\b(\w+(?:\s+\w+)?)\s+(?:\1\s*){2,}', r'\1', line)
        
        # Match patterns like "[-o file.yaml] [-o file.yaml] [-o file.yaml]"
        result = re.sub(r'(\[.*?\])\s*(?:\1\s*){1,}', r'\1', result)
        
        # Japanese repetition patterns (ますます, ですがですが, しかししかし, etc.)
        result = re.sub(r'(ます){3,}', 'ます', result)
        result = re.sub(r'(です){3,}', 'です', result)
        result = re.sub(r'(ですが){2,}', 'ですが', result)
        result = re.sub(r'(しかし){2,}', 'しかし', result)
        result = re.sub(r'(However\s*){2,}', 'However ', result)
        
        # Generic: any 2+ char sequence repeated 3+ times
        result = re.sub(r'(.{2,}?)\1{2,}', r'\1', result)
        
        return result
    
    def _translate_single_language(self, content: str, language: str, mode: str) -> Tuple[str, str, Optional[str]]:
        """
        Translate content to a single language
        
        Args:
            content: Content to translate
            language: Target language code
            mode: Translation mode
            
        Returns:
            Tuple[str, str, Optional[str]]: (language_code, translated_content, error_message)
        """
        language_name = self.get_language_name(language)
        info(f"Translating to {language_name} ({language})...")
        
        prompt = self._build_single_language_prompt(content, language, mode)
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        language_name = self.get_language_name(language)
        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": f"You are a Markdown translator. Translate into {language_name}. Output ONLY the translated document. No language headers. No notes. No code block wrappers. Keep all formatting unchanged."
                },
                {
                    "role": "user", 
                    "content": prompt
                }
            ],
            "stream": False,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
            "top_p": self.top_p,
            "top_k": self.top_k,
            "frequency_penalty": self.frequency_penalty,
            "n": 1,
            "response_format": {"type": "text"}
        }
        
        try:
            debug(f"[{language}] Sending request to: {self.API_URL}")
            
            response = requests.post(
                self.API_URL,
                json=payload,
                headers=headers,
                timeout=self.timeout
            )
            
            debug(f"[{language}] Response status code: {response.status_code}")
            
            if response.status_code != 200:
                error_msg = response.text
                error(f"[{language}] API error: {error_msg}")
                return (language, "", f"API error: {response.status_code}")
            
            result = response.json()
            
            if "error" in result:
                error_msg = result["error"].get("message", "Unknown error")
                return (language, "", f"API error: {error_msg}")
            
            translated_content = result["choices"][0]["message"]["content"]
            
            # Post-process: clean up unwanted patterns
            translated_content = self._clean_translation_output(translated_content)
            
            # Log usage info
            if "usage" in result:
                usage = result["usage"]
                info(f"[{language}] API usage - prompt_tokens: {usage.get('prompt_tokens', 0)}, completion_tokens: {usage.get('completion_tokens', 0)}")
            
            info(f"[{language}] Translation completed, length: {len(translated_content)}")
            debug(f"[{language}] ========== Response Start ==========")
            debug(f"{translated_content[:500]}..." if len(translated_content) > 500 else translated_content)
            debug(f"[{language}] ========== Response End ==========")
            
            return (language, translated_content, None)
            
        except requests.exceptions.Timeout:
            return (language, "", f"Request timeout after {self.timeout}s")
        except requests.exceptions.RequestException as e:
            return (language, "", f"Network error: {e}")
        except Exception as e:
            return (language, "", f"Translation failed: {e}")
    
    def translate(self, content: str, languages: List[str], **kwargs) -> str:
        """
        Execute translation using SiliconFlow API with parallel requests
        
        Args:
            content: Content to translate
            languages: Target language list
            **kwargs: Additional parameters (mode, etc.)
            
        Returns:
            str: JSON string with translations for each language
        """
        if not self.validate_credentials():
            raise Exception("SiliconFlow API key not configured")
        
        mode = kwargs.get("mode", "gen")
        results: Dict[str, str] = {}
        errors: List[str] = []
        
        # For English, use original content directly (no translation needed)
        languages_to_translate = []
        for lang in languages:
            if lang == "en":
                results["en"] = content
                info(f"✓ en: Using original content (no translation needed)")
            else:
                languages_to_translate.append(lang)
        
        if not languages_to_translate:
            # All languages are English, return directly
            json_result = json.dumps(results, ensure_ascii=False, indent=2)
            return json_result
        
        info(f"Starting parallel translation for {len(languages_to_translate)} languages: {', '.join(languages_to_translate)}")
        
        # Use ThreadPoolExecutor for parallel requests
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit all translation tasks
            future_to_lang = {
                executor.submit(self._translate_single_language, content, lang, mode): lang 
                for lang in languages_to_translate
            }
            
            # Collect results as they complete
            for future in as_completed(future_to_lang):
                lang = future_to_lang[future]
                try:
                    language, translated, err = future.result()
                    if err:
                        errors.append(f"[{language}] {err}")
                        warning(f"Translation failed for {language}: {err}")
                    else:
                        results[language] = translated
                        info(f"✓ {language} translation completed")
                except Exception as e:
                    errors.append(f"[{lang}] Unexpected error: {e}")
                    error(f"Unexpected error for {lang}: {e}")
        
        # Report results
        info(f"Translation completed: {len(results)} successful, {len(errors)} failed")
        if errors:
            for err in errors:
                warning(err)
        
        # Return as JSON string for compatibility with existing parser
        json_result = json.dumps(results, ensure_ascii=False, indent=2)
        debug(f"Final JSON result length: {len(json_result)}")
        
        return json_result
    
    def validate_credentials(self) -> bool:
        """
        Validate if SiliconFlow API key is configured
        
        Returns:
            bool: Whether credentials are valid
        """
        if not self.api_key:
            error("SiliconFlow API key not configured. Set SILICONFLOW_API_KEY environment variable.")
            return False
        return True
    
    def list_available_models(self) -> List[str]:
        """
        List commonly used SiliconFlow models
        
        Returns:
            List[str]: Available model names
        """
        return [
            "deepseek-ai/DeepSeek-R1-0528-Qwen3-8B",
            "deepseek-ai/DeepSeek-V2.5",
            "Qwen/Qwen2.5-7B-Instruct",
            "Qwen/Qwen2.5-72B-Instruct",
            "meta-llama/Meta-Llama-3.1-8B-Instruct",
            "meta-llama/Meta-Llama-3.1-70B-Instruct",
        ]
