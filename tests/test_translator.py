"""
Translator test module

Tests translator functionality.
"""

import pytest
from pathlib import Path
from unittest.mock import Mock, patch
from src.core.translator import Translator
from src.utils.config import Config
from src.models.types import TranslationResponse


class TestTranslator:
    """Translator test class"""
    
    def setup_method(self):
        """Set up test environment"""
        self.config = Config()
        self.translator = Translator(self.config)
    
    def test_init(self):
        """Test initialization"""
        assert self.translator.config is not None
        assert self.translator.tencent_service is not None
        assert self.translator.sse_client is not None
    
    def test_get_supported_languages(self):
        """Test getting supported language list"""
        languages = self.translator.get_supported_languages()
        assert isinstance(languages, list)
        assert len(languages) > 0
        assert "zh-Hans" in languages
        assert "en" in languages
    
    @patch('src.core.translator.Path')
    @patch('src.core.translator.FileUtils.get_project_files')
    def test_read_project_content_success(self, mock_get_files, mock_path):
        """Test successful project content reading"""
        # Mock the file utils to return a README file
        mock_readme_path = Mock()
        mock_readme_path.name = "README.md"
        mock_readme_path.read_text.return_value = "# Test README"
        mock_readme_path.relative_to.return_value = "README.md"
        
        mock_get_files.return_value = [mock_readme_path]
        
        content = self.translator._read_project_content("test_project")
        assert "=== README.md ===" in content
        assert "# Test README" in content
    
    @patch('src.core.translator.Path')
    def test_read_project_content_missing_files(self, mock_path):
        """Test reading non-existent project files"""
        # Simulate file doesn't exist
        mock_readme = Mock()
        mock_readme.exists.return_value = False
        
        mock_src = Mock()
        mock_src.exists.return_value = False
        
        mock_path.return_value.__truediv__.side_effect = lambda x: {
            "README.md": mock_readme,
            "src": mock_src,
            ".gitignore": Mock(exists=lambda: False)
        }[x]
        
        content = self.translator._read_project_content("test_project")
        assert content == ""
    
    def test_build_translation_request(self):
        """Test building translation request"""
        content = "Test content"
        languages = ["中文", "English"]
        
        request = self.translator._build_translation_request(content, languages)
        
        assert request.content is not None
        assert "中文" in request.content
        assert "English" in request.content
        assert request.languages == languages
    
    @patch('src.services.sse_client.SSEClient.send_request')
    def test_execute_translation_success(self, mock_send_request):
        """Test successful translation execution"""
        mock_send_request.return_value = "Translated content"
        
        request = Mock()
        request.languages = ["中文", "English"]
        
        response = self.translator._execute_translation(request)
        
        assert response.success is True
        assert response.content == "Translated content"
        assert response.languages == ["中文", "English"]
    
    @patch('src.services.sse_client.SSEClient.send_request')
    def test_execute_translation_failure(self, mock_send_request):
        """Test translation failure"""
        mock_send_request.side_effect = Exception("Network error")
        
        request = Mock()
        request.languages = ["中文", "English"]
        
        response = self.translator._execute_translation(request)
        
        assert response.success is False
        assert "Network error" in response.error
        assert response.languages == ["中文", "English"]
    
    @patch.object(Translator, '_read_project_content')
    @patch.object(Translator, '_build_translation_request')
    @patch.object(Translator, '_execute_translation')
    def test_translate_project_success(self, mock_execute, mock_build, mock_read):
        """Test successful project translation"""
        # Set mock return values
        mock_read.return_value = "Project content"
        
        mock_request = Mock()
        mock_build.return_value = mock_request
        
        mock_response = TranslationResponse(
            success=True,
            content="Translated content",
            languages=["中文", "English"]
        )
        mock_execute.return_value = mock_response
        
        # Execute test
        result = self.translator.translate_project("test_project", ["中文", "English"])
        
        # Verify results
        assert result.success is True
        assert result.content == "Translated content"
        assert result.languages == ["中文", "English"]
        
        # Verify method calls
        mock_read.assert_called_once_with("test_project")
        mock_build.assert_called_once_with("Project content", ["中文", "English"])
        mock_execute.assert_called_once_with(mock_request) 