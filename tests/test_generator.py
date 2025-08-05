"""
生成器测试模块

测试生成器的功能，特别是英文README放在根目录的逻辑。
"""

import pytest
from pathlib import Path
from unittest.mock import Mock, patch
from src.core.generator import Generator
from src.models.types import ParsedReadme, GenerationResult


class TestGenerator:
    """生成器测试类"""
    
    def setup_method(self):
        """设置测试环境"""
        self.generator = Generator()
    
    def test_init(self):
        """测试初始化"""
        assert self.generator.output_dir == Path("docs")
        assert self.generator.file_utils is not None
    
    def test_get_filename_for_language_english(self):
        """测试英文文件名生成"""
        # 测试英文应该返回README.md
        filename = self.generator._get_filename_for_language("English")
        assert filename == "README.md"
        
        # 测试简写形式
        filename = self.generator._get_filename_for_language("en")
        assert filename == "README.md"
    
    def test_get_filename_for_language_other_languages(self):
        """测试其他语言文件名生成"""
        # 测试中文
        filename = self.generator._get_filename_for_language("中文")
        assert filename == "README.zh.md"
        
        # 测试日文
        filename = self.generator._get_filename_for_language("日本語")
        assert filename == "README.ja.md"
        
        # 测试未知语言
        filename = self.generator._get_filename_for_language("unknown")
        assert filename == "README.unknown.md"
    
    def test_get_language_from_filename(self):
        """测试从文件名获取语言"""
        # 测试根目录的README.md
        lang = self.generator._get_language_from_filename("README.md")
        assert lang == "English"
        
        # 测试中文
        lang = self.generator._get_language_from_filename("README.zh.md")
        assert lang == "中文"
        
        # 测试未知文件名
        lang = self.generator._get_language_from_filename("unknown.md")
        assert lang is None
    
    @patch('src.core.generator.FileUtils.write_text_file')
    @patch('src.core.generator.Path.mkdir')
    def test_generate_readme_files_english_in_root(self, mock_mkdir, mock_write):
        """测试英文README放在根目录"""
        # 准备测试数据
        parsed_readme = ParsedReadme(
            content={
                "en": "# Project README\n\n## Introduction\nThis is English content",
                "zh": "# 项目 README\n\n## 介绍\n这是中文内容",
                "ja": "# プロジェクト README\n\n## はじめに\nこれは日本語の内容です"
            },
            languages=["en", "zh", "ja"],
            total_count=3
        )
        
        # 执行测试
        result = self.generator.generate_readme_files(parsed_readme)
        
        # 验证结果
        assert result.total_saved == 3
        assert result.total_failed == 0
        
        # 验证英文README保存在根目录
        english_file = next(f for f in result.saved_files if f["language"] == "en")
        assert english_file["filename"] == "README.md"
        assert english_file["filepath"] == "README.md"
        
        # 验证中文README保存在docs目录
        chinese_file = next(f for f in result.saved_files if f["language"] == "zh")
        assert chinese_file["filename"] == "README.zh.md"
        assert chinese_file["filepath"] == "docs/README.zh.md"
        
        # 验证日文README保存在docs目录
        japanese_file = next(f for f in result.saved_files if f["language"] == "ja")
        assert japanese_file["filename"] == "README.ja.md"
        assert japanese_file["filepath"] == "docs/README.ja.md"
        
        # 验证文件写入调用
        assert mock_write.call_count == 3
        
        # 验证英文文件写入调用
        english_call = next(call for call in mock_write.call_args_list 
                          if call[0][0] == Path("README.md"))
        expected_content = "> This is the English README. For other language versions, please see the [docs](./docs) directory.\n\n# Project README\n\n## Introduction\nThis is English content"
        assert english_call[0][1] == expected_content
        
        # 验证中文文件写入调用
        chinese_call = next(call for call in mock_write.call_args_list 
                          if call[0][0] == Path("docs/README.zh.md"))
        assert chinese_call[0][1] == "# 项目 README\n\n## 介绍\n这是中文内容"
        
        # 验证日文文件写入调用
        japanese_call = next(call for call in mock_write.call_args_list 
                           if call[0][0] == Path("docs/README.ja.md"))
        assert japanese_call[0][1] == "# プロジェクト README\n\n## はじめに\nこれは日本語の内容です"
    
    @patch('src.core.generator.FileUtils.write_text_file')
    def test_generate_readme_files_write_failure(self, mock_write):
        """测试文件写入失败的情况"""
        # 模拟写入失败
        mock_write.side_effect = Exception("Write error")
        
        parsed_readme = ParsedReadme(
            content={"English": "# Test content"},
            languages=["English"],
            total_count=1
        )
        
        # 执行测试
        result = self.generator.generate_readme_files(parsed_readme)
        
        # 验证结果
        assert result.total_saved == 0
        assert result.total_failed == 1
        
        failed_file = result.failed_files[0]
        assert failed_file["language"] == "English"
        assert failed_file["filename"] == "README.md"
        assert "Write error" in failed_file["error"]
    
    def test_generate_summary_with_english_in_root(self):
        """测试生成总结报告，包含英文README在根目录的信息"""
        # 准备测试数据
        generation_result = GenerationResult(
            saved_files=[
                {
                    "language": "en",
                    "filename": "README.md",
                    "filepath": "README.md",
                    "size": 100
                },
                {
                    "language": "zh",
                    "filename": "README.zh.md",
                    "filepath": "docs/README.zh.md",
                    "size": 150
                }
            ],
            failed_files=[],
            total_saved=2,
            total_failed=0
        )
        
        # 执行测试
        summary = self.generator.generate_summary(generation_result)
        
        # 验证总结内容
        assert "README.md (100 bytes) - 根目录" in summary
        assert "README.zh.md (150 bytes) - docs目录" in summary
        assert "成功生成了 2 种语言的 README" in summary
        assert "en" in summary
        assert "zh" in summary
    
    @patch('src.core.generator.Path.glob')
    @patch('src.core.generator.Path.unlink')
    def test_cleanup_old_files(self, mock_unlink, mock_glob):
        """测试清理旧文件"""
        # 模拟存在的文件
        mock_glob.return_value = [
            Path("docs/README.zh.md"),
            Path("docs/README.ja.md"),
            Path("docs/README.fr.md")
        ]
        
        # 执行清理，只保留中文和日文
        self.generator.cleanup_old_files(["中文", "日本語"])
        
        # 验证只删除了法文文件
        assert mock_unlink.call_count == 1
    
    def test_parse_json_format(self):
        """测试JSON格式的解析"""
        from src.core.parser import Parser
        
        parser = Parser()
        
        # 测试JSON格式的响应
        json_response = '''{
            "English readme": "# Project Overview\\n\\nThis is English content.",
            "Chinese readme": "# 项目概述\\n\\n这是中文内容。",
            "Japanese readme": "# プロジェクト概要\\n\\nこれは日本語の内容です。"
        }'''
        
        result = parser.parse_multilingual_content(json_response)
        
        # 验证解析结果
        assert result.total_count == 3
        assert "en" in result.languages
        assert "zh" in result.languages
        assert "ja" in result.languages
        
        # 验证内容
        assert "# Project Overview" in result.content["en"]
        assert "# 项目概述" in result.content["zh"]
        assert "# プロジェクト概要" in result.content["ja"]
    
    def test_json_key_mapping(self):
        """测试JSON键到语言代码的映射"""
        from src.core.parser import Parser
        
        parser = Parser()
        
        # 测试各种JSON键的映射
        assert parser._map_json_key_to_language("English readme") == "en"
        assert parser._map_json_key_to_language("Chinese readme") == "zh"
        assert parser._map_json_key_to_language("Japanese readme") == "ja"
        assert parser._map_json_key_to_language("Korean readme") == "ko"
        assert parser._map_json_key_to_language("French readme") == "fr"
        assert parser._map_json_key_to_language("German readme") == "de"
        assert parser._map_json_key_to_language("Spanish readme") == "es"
        assert parser._map_json_key_to_language("Italian readme") == "it"
        assert parser._map_json_key_to_language("Portuguese readme") == "pt"
        assert parser._map_json_key_to_language("Russian readme") == "ru"
        
        # 测试未知键
        assert parser._map_json_key_to_language("Unknown readme") is None 