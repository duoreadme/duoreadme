"""
文档生成器模块

负责生成和保存多语言README文件。
"""

import os
from pathlib import Path
from typing import Dict, List, Optional
from ..utils.file_utils import FileUtils
from ..models.types import ParsedReadme, GenerationResult


class Generator:
    """文档生成器类，负责生成和保存多语言README文件"""
    
    def __init__(self):
        """
        初始化生成器
        """
        self.output_dir = Path("docs")
        self.file_utils = FileUtils()
        
    def generate_readme_files(self, parsed_readme: ParsedReadme, raw_content: str = "") -> GenerationResult:
        """
        生成多语言README文件
        
        Args:
            parsed_readme: 解析后的README对象
            raw_content: 原始响应内容（不再保存）
            
        Returns:
            GenerationResult: 生成结果对象
        """
        # 确保输出目录存在
        self._ensure_output_directory()
        
        saved_files = []
        failed_files = []
        
        # 保存各语言的README文件
        for lang, content in parsed_readme.content.items():
            filename = self._get_filename_for_language(lang)
            filepath = self.output_dir / filename
            
            try:
                self.file_utils.write_text_file(filepath, content)
                saved_files.append({
                    "language": lang,
                    "filename": filename,
                    "filepath": str(filepath),
                    "size": len(content)
                })
                print(f"已保存 {lang} README 到 {filepath}")
            except Exception as e:
                failed_files.append({
                    "language": lang,
                    "filename": filename,
                    "error": str(e)
                })
                print(f"保存 {lang} README 失败: {e}")
        

        
        return GenerationResult(
            saved_files=saved_files,
            failed_files=failed_files,
            total_saved=len(saved_files),
            total_failed=len(failed_files)
        )
    
    def _ensure_output_directory(self):
        """确保输出目录存在"""
        if not self.output_dir.exists():
            self.output_dir.mkdir(parents=True)
            print(f"✓ 创建 {self.output_dir} 目录")
        else:
            print(f"✓ {self.output_dir} 目录已存在")
    
    def _get_filename_for_language(self, language: str) -> str:
        """
        获取指定语言对应的文件名
        
        Args:
            language: 语言名称
            
        Returns:
            str: 对应的文件名
        """
        filename_map = {
            "中文": "README.zh.md",
            "English": "README.en.md", 
            "日本語": "README.ja.md",
            "한국어": "README.ko.md",
            "Français": "README.fr.md",
            "Deutsch": "README.de.md",
            "Español": "README.es.md",
            "Italiano": "README.it.md",
            "Português": "README.pt.md",
            "Русский": "README.ru.md"
        }
        
        return filename_map.get(language, f"README.{language.lower()}.md")
    
    def generate_summary(self, generation_result: GenerationResult) -> str:
        """
        生成总结报告
        
        Args:
            generation_result: 生成结果对象
            
        Returns:
            str: 总结报告文本
        """
        summary_lines = [
            "=" * 60,
            "项目翻译和解析完成总结",
            "=" * 60,
            f"✓ {self.output_dir} 目录已创建",
            "生成的文件:"
        ]
        
        # 添加生成的文件信息
        for file_info in generation_result.saved_files:
            if file_info["language"] != "raw":
                summary_lines.append(f"  - {file_info['filename']} ({file_info['size']} bytes)")
        
        # 添加原始响应文件
        raw_files = [f for f in generation_result.saved_files if f["language"] == "raw"]
        for file_info in raw_files:
            summary_lines.append(f"  - {file_info['filename']} ({file_info['size']} bytes)")
        
        # 添加成功生成的语言列表
        languages = [f["language"] for f in generation_result.saved_files if f["language"] != "raw"]
        if languages:
            summary_lines.append(f"✓ 成功生成了 {len(languages)} 种语言的 README:")
            for lang in languages:
                summary_lines.append(f"  - {lang}")
        
        # 添加失败信息
        if generation_result.failed_files:
            summary_lines.append("失败的文件:")
            for file_info in generation_result.failed_files:
                summary_lines.append(f"  - {file_info['filename']}: {file_info['error']}")
        
        summary_lines.extend([
            "=" * 60,
            "任务完成！",
            "=" * 60
        ])
        
        return "\n".join(summary_lines)
    
    def cleanup_old_files(self, keep_languages: Optional[List[str]] = None):
        """
        清理旧的文件
        
        Args:
            keep_languages: 要保留的语言列表，如果为None则保留所有
        """
        if keep_languages is None:
            return
        
        # 获取要删除的文件
        files_to_delete = []
        for file_path in self.output_dir.glob("README.*.md"):
            lang = self._get_language_from_filename(file_path.name)
            if lang and lang not in keep_languages:
                files_to_delete.append(file_path)
        
        # 删除文件
        for file_path in files_to_delete:
            try:
                file_path.unlink()
                print(f"已删除旧文件: {file_path}")
            except Exception as e:
                print(f"删除文件失败 {file_path}: {e}")
    
    def _get_language_from_filename(self, filename: str) -> Optional[str]:
        """
        从文件名获取语言
        
        Args:
            filename: 文件名
            
        Returns:
            Optional[str]: 语言名称，如果无法识别则返回None
        """
        filename_map = {
            "README.zh.md": "中文",
            "README.en.md": "English",
            "README.ja.md": "日本語",
            "README.ko.md": "한국어",
            "README.fr.md": "Français",
            "README.de.md": "Deutsch",
            "README.es.md": "Español",
            "README.it.md": "Italiano",
            "README.pt.md": "Português",
            "README.ru.md": "Русский"
        }
        
        return filename_map.get(filename) 