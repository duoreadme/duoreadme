"""
Generator test module

Tests generator functionality, especially the logic for placing English README in root directory.
"""

import pytest
from pathlib import Path
from unittest.mock import Mock, patch
from src.core.generator import Generator
from src.models.types import ParsedReadme, GenerationResult


class TestGenerator:
    """Generator test class"""
    
    def setup_method(self):
        """Set up test environment"""
        self.generator = Generator()
    
    def test_init(self):
        """Test initialization"""
        assert self.generator.output_dir == Path("docs")
        assert self.generator.file_utils is not None
    
    def test_get_filename_for_language_english(self):
        """Test English filename generation"""
        # Test English should return README.md
        filename = self.generator._get_filename_for_language("English")
        assert filename == "README.md"
        
        # Test abbreviated form
        filename = self.generator._get_filename_for_language("en")
        assert filename == "README.md"
    
    def test_get_filename_for_language_other_languages(self):
        """Test other language filename generation"""
        # Test Chinese
        filename = self.generator._get_filename_for_language("中文")
        assert filename == "README.zh.md"
        
        # Test Japanese
        filename = self.generator._get_filename_for_language("日本語")
        assert filename == "README.ja.md"
        
        # Test unknown language
        filename = self.generator._get_filename_for_language("unknown")
        assert filename == "README.unknown.md"
    
    def test_get_language_from_filename(self):
        """Test getting language from filename"""
        # Test README.md in root directory
        lang = self.generator._get_language_from_filename("README.md")
        assert lang == "English"
        
        # Test Chinese
        lang = self.generator._get_language_from_filename("README.zh.md")
        assert lang == "中文"
        
        # Test unknown filename
        lang = self.generator._get_language_from_filename("unknown.md")
        assert lang is None
    
    @patch('src.core.generator.FileUtils.write_text_file')
    @patch('src.core.generator.Path.mkdir')
    def test_generate_readme_files_english_in_root(self, mock_mkdir, mock_write):
        """Test English README placed in root directory"""
        # Prepare test data
        parsed_readme = ParsedReadme(
            content={
                "en": "# Project README\n\n## Introduction\nThis is English content",
                "zh": "# 项目 README\n\n## 介绍\n这是中文内容",
                "ja": "# プロジェクト README\n\n## はじめに\nこれは日本語の内容です"
            },
            languages=["en", "zh", "ja"],
            total_count=3
        )
        
        # Execute test
        result = self.generator.generate_readme_files(parsed_readme)
        
        # Verify results
        assert result.total_saved == 3
        assert result.total_failed == 0
        
        # Verify English README saved in root directory
        english_file = next(f for f in result.saved_files if f["language"] == "en")
        assert english_file["filename"] == "README.md"
        assert english_file["filepath"] == "README.md"
        
        # Verify Chinese README saved in docs directory
        chinese_file = next(f for f in result.saved_files if f["language"] == "zh")
        assert chinese_file["filename"] == "README.zh.md"
        assert chinese_file["filepath"] == "docs/README.zh.md"
        
        # Verify Japanese README saved in docs directory
        japanese_file = next(f for f in result.saved_files if f["language"] == "ja")
        assert japanese_file["filename"] == "README.ja.md"
        assert japanese_file["filepath"] == "docs/README.ja.md"
        
        # Verify file write calls
        assert mock_write.call_count == 3
        
        # Verify English file write call
        english_call = next(call for call in mock_write.call_args_list 
                          if call[0][0] == Path("README.md"))
        expected_content = "> This is the English README. You can view the [简体中文](./docs/README.zh.md) | [日本語](./docs/README.ja.md) versions.\n\n# Project README\n\n## Introduction\nThis is English content"
        assert english_call[0][1] == expected_content
        
        # Verify Chinese file write call
        chinese_call = next(call for call in mock_write.call_args_list 
                          if call[0][0] == Path("docs/README.zh.md"))
        assert chinese_call[0][1] == "# 项目 README\n\n## 介绍\n这是中文内容"
        
        # Verify Japanese file write call
        japanese_call = next(call for call in mock_write.call_args_list 
                           if call[0][0] == Path("docs/README.ja.md"))
        assert japanese_call[0][1] == "# プロジェクト README\n\n## はじめに\nこれは日本語の内容です"
    
    @patch('src.core.generator.FileUtils.write_text_file')
    def test_generate_readme_files_write_failure(self, mock_write):
        """Test file write failure scenario"""
        # Simulate write failure
        mock_write.side_effect = Exception("Write error")
        
        parsed_readme = ParsedReadme(
            content={"English": "# Test content"},
            languages=["English"],
            total_count=1
        )
        
        # Execute test
        result = self.generator.generate_readme_files(parsed_readme)
        
        # Verify results
        assert result.total_saved == 0
        assert result.total_failed == 1
        
        failed_file = result.failed_files[0]
        assert failed_file["language"] == "English"
        assert failed_file["filename"] == "README.md"
        assert "Write error" in failed_file["error"]
    
    def test_generate_summary_with_english_in_root(self):
        """Test generating summary report, including information about English README in root directory"""
        # Prepare test data
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
        
        # Execute test
        summary = self.generator.generate_summary(generation_result)
        
        # Verify summary content
        assert "README.md (100 bytes) - root directory" in summary
        assert "README.zh.md (150 bytes) - docs directory" in summary
        assert "Successfully generated README in 2 languages" in summary
        assert "en" in summary
        assert "zh" in summary
    
    @patch('src.core.generator.Path.glob')
    @patch('src.core.generator.Path.unlink')
    def test_cleanup_old_files(self, mock_unlink, mock_glob):
        """Test cleaning up old files"""
        # Simulate existing files
        mock_glob.return_value = [
            Path("docs/README.zh.md"),
            Path("docs/README.ja.md"),
            Path("docs/README.fr.md")
        ]
        
        # Execute cleanup, only keep Chinese and Japanese
        self.generator.cleanup_old_files(["中文", "日本語"])
        
        # Verify only French file was deleted
        assert mock_unlink.call_count == 1
    
    def test_parse_json_format(self):
        """Test JSON format parsing"""
        from src.core.parser import Parser
        
        parser = Parser()
        
        # Test JSON format response
        json_response = '''{
            "English readme": "# Project Overview\\n\\nThis is English content.",
            "Chinese readme": "# 项目概述\\n\\n这是中文内容。",
            "Japanese readme": "# プロジェクト概要\\n\\nこれは日本語の内容です。"
        }'''
        
        result = parser.parse_multilingual_content(json_response)
        
        # Verify parsing results
        assert result.total_count == 3
        assert "en" in result.languages
        assert "zh-Hans" in result.languages
        assert "ja" in result.languages
        
        # Verify content
        assert "# Project Overview" in result.content["en"]
        assert "# 项目概述" in result.content["zh-Hans"]
        assert "# プロジェクト概要" in result.content["ja"]
    
    def test_json_key_mapping(self):
        """Test JSON key to language code mapping"""
        from src.core.parser import Parser
        
        parser = Parser()
        
        # Test various JSON key mappings
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
        
        # Test unknown key
        assert parser._map_json_key_to_language("Unknown readme") is None 