"""
File operation utility module

Provides file read/write and operation utility functions.
"""

import os
import shutil
import fnmatch
from pathlib import Path
from typing import List, Optional, Union


class FileUtils:
    """File operation utility class"""
    
    def read_text_file(self, file_path: Union[str, Path], encoding: str = "utf-8") -> str:
        """
        Read text file
        
        Args:
            file_path: File path
            encoding: File encoding
            
        Returns:
            File content
            
        Raises:
            FileNotFoundError: File does not exist
            UnicodeDecodeError: Encoding error
        """
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"File does not exist: {file_path}")
        
        try:
            return file_path.read_text(encoding=encoding)
        except UnicodeDecodeError as e:
            raise UnicodeDecodeError(f"File encoding error {file_path}: {e}")
    
    def write_text_file(self, file_path: Union[str, Path], content: str, encoding: str = "utf-8"):
        """
        Write text file
        
        Args:
            file_path: File path
            content: Content to write
            encoding: File encoding
            
        Raises:
            OSError: Write failed
        """
        file_path = Path(file_path)
        
        # Ensure directory exists
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            file_path.write_text(content, encoding=encoding)
        except OSError as e:
            raise OSError(f"Failed to write file {file_path}: {e}")
    
    def read_binary_file(self, file_path: Union[str, Path]) -> bytes:
        """
        Read binary file
        
        Args:
            file_path: File path
            
        Returns:
            File content
            
        Raises:
            FileNotFoundError: File does not exist
        """
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"File does not exist: {file_path}")
        
        return file_path.read_bytes()
    
    def write_binary_file(self, file_path: Union[str, Path], content: bytes):
        """
        Write binary file
        
        Args:
            file_path: File path
            content: Content to write
            
        Raises:
            OSError: Write failed
        """
        file_path = Path(file_path)
        
        # Ensure directory exists
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            file_path.write_bytes(content)
        except OSError as e:
            raise OSError(f"Failed to write file {file_path}: {e}")
    
    def copy_file(self, src: Union[str, Path], dst: Union[str, Path]):
        """
        Copy file
        
        Args:
            src: Source file path
            dst: Destination file path
            
        Raises:
            FileNotFoundError: Source file does not exist
            OSError: Copy failed
        """
        src = Path(src)
        dst = Path(dst)
        
        if not src.exists():
            raise FileNotFoundError(f"Source file does not exist: {src}")
        
        # Ensure destination directory exists
        dst.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            shutil.copy2(src, dst)
        except OSError as e:
            raise OSError(f"Failed to copy file {src} -> {dst}: {e}")
    
    def move_file(self, src: Union[str, Path], dst: Union[str, Path]):
        """
        Move file
        
        Args:
            src: Source file path
            dst: Destination file path
            
        Raises:
            FileNotFoundError: Source file does not exist
            OSError: Move failed
        """
        src = Path(src)
        dst = Path(dst)
        
        if not src.exists():
            raise FileNotFoundError(f"Source file does not exist: {src}")
        
        # Ensure destination directory exists
        dst.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            shutil.move(str(src), str(dst))
        except OSError as e:
            raise OSError(f"Failed to move file {src} -> {dst}: {e}")
    
    def delete_file(self, file_path: Union[str, Path]):
        """
        Delete file
        
        Args:
            file_path: File path
            
        Raises:
            FileNotFoundError: File does not exist
            OSError: Delete failed
        """
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"File does not exist: {file_path}")
        
        try:
            file_path.unlink()
        except OSError as e:
            raise OSError(f"Failed to delete file {file_path}: {e}")
    
    def create_directory(self, dir_path: Union[str, Path], exist_ok: bool = True):
        """
        Create directory
        
        Args:
            dir_path: Directory path
            exist_ok: Whether to not raise error if directory already exists
            
        Raises:
            OSError: Creation failed
        """
        dir_path = Path(dir_path)
        
        try:
            dir_path.mkdir(parents=True, exist_ok=exist_ok)
        except OSError as e:
            raise OSError(f"Failed to create directory {dir_path}: {e}")
    
    def delete_directory(self, dir_path: Union[str, Path], recursive: bool = False):
        """
        Delete directory
        
        Args:
            dir_path: Directory path
            recursive: Whether to delete recursively
            
        Raises:
            FileNotFoundError: Directory does not exist
            OSError: Delete failed
        """
        dir_path = Path(dir_path)
        
        if not dir_path.exists():
            raise FileNotFoundError(f"Directory does not exist: {dir_path}")
        
        try:
            if recursive:
                shutil.rmtree(dir_path)
            else:
                dir_path.rmdir()
        except OSError as e:
            raise OSError(f"Failed to delete directory {dir_path}: {e}")
    
    def list_files(self, dir_path: Union[str, Path], pattern: str = "*", recursive: bool = False) -> List[Path]:
        """
        List files in directory
        
        Args:
            dir_path: Directory path
            pattern: File matching pattern
            recursive: Whether to search recursively
            
        Returns:
            List of file paths
            
        Raises:
            FileNotFoundError: Directory does not exist
        """
        dir_path = Path(dir_path)
        
        if not dir_path.exists():
            raise FileNotFoundError(f"Directory does not exist: {dir_path}")
        
        if not dir_path.is_dir():
            raise NotADirectoryError(f"Not a directory: {dir_path}")
        
        if recursive:
            return list(dir_path.rglob(pattern))
        else:
            return list(dir_path.glob(pattern))
    
    def get_file_size(self, file_path: Union[str, Path]) -> int:
        """
        Get file size
        
        Args:
            file_path: File path
            
        Returns:
            File size in bytes
            
        Raises:
            FileNotFoundError: File does not exist
        """
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"File does not exist: {file_path}")
        
        return file_path.stat().st_size
    
    def get_file_info(self, file_path: Union[str, Path]) -> dict:
        """
        Get file information
        
        Args:
            file_path: File path
            
        Returns:
            File information dictionary
            
        Raises:
            FileNotFoundError: File does not exist
        """
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"File does not exist: {file_path}")
        
        stat = file_path.stat()
        
        return {
            "name": file_path.name,
            "path": str(file_path),
            "size": stat.st_size,
            "created_time": stat.st_ctime,
            "modified_time": stat.st_mtime,
            "is_file": file_path.is_file(),
            "is_dir": file_path.is_dir(),
            "extension": file_path.suffix
        }
    
    def ensure_directory_exists(self, dir_path: Union[str, Path]):
        """
        Ensure directory exists, create if it doesn't exist
        
        Args:
            dir_path: Directory path
        """
        dir_path = Path(dir_path)
        dir_path.mkdir(parents=True, exist_ok=True)
    
    def is_text_file(self, file_path: Union[str, Path]) -> bool:
        """
        Determine if it's a text file
        
        Args:
            file_path: File path
            
        Returns:
            Whether it's a text file
        """
        file_path = Path(file_path)
        
        if not file_path.exists() or not file_path.is_file():
            return False
        
        # Check file extension
        text_extensions = {
            '.txt', '.md', '.py', '.js', '.ts', '.html', '.css', '.json', 
            '.xml', '.yaml', '.yml', '.ini', '.cfg', '.conf', '.log'
        }
        
        if file_path.suffix.lower() in text_extensions:
            return True
        
        # Try to read file beginning to determine if it's text
        try:
            with open(file_path, 'rb') as f:
                chunk = f.read(1024)
                return chunk.decode('utf-8', errors='ignore').isprintable()
        except:
            return False
    
    def parse_gitignore(self, gitignore_path: Union[str, Path]) -> List[str]:
        """
        Parse .gitignore file
        
        Args:
            gitignore_path: .gitignore file path
            
        Returns:
            List of ignore patterns
        """
        gitignore_path = Path(gitignore_path)
        patterns = []
        
        if not gitignore_path.exists():
            return patterns
        
        try:
            with open(gitignore_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    # Skip empty lines and comments
                    if line and not line.startswith('#'):
                        patterns.append(line)
        except Exception as e:
            print(f"Warning: Failed to read .gitignore file: {e}")
        
        return patterns
    
    def should_ignore_file(self, file_path: Union[str, Path], gitignore_patterns: List[str], base_path: Union[str, Path]) -> bool:
        """
        Determine if file should be ignored
        
        Args:
            file_path: File path
            gitignore_patterns: .gitignore pattern list
            base_path: Base path (directory where .gitignore file is located)
            
        Returns:
            Whether it should be ignored
        """
        file_path = Path(file_path)
        base_path = Path(base_path)
        
        # Calculate relative path to base path
        try:
            relative_path = file_path.relative_to(base_path)
        except ValueError:
            # If file is not under base path, don't ignore
            return False
        
        # Convert to string, use forward slash separator (gitignore standard)
        relative_path_str = str(relative_path).replace('\\', '/')
        
        for pattern in gitignore_patterns:
            # Handle directory patterns (ending with /)
            if pattern.endswith('/'):
                if relative_path_str.startswith(pattern[:-1]) or fnmatch.fnmatch(relative_path_str, pattern[:-1]):
                    return True
            
            # Handle file patterns
            if fnmatch.fnmatch(relative_path_str, pattern):
                return True
            
            # Handle wildcard patterns
            if fnmatch.fnmatch(relative_path_str, pattern):
                return True
        
        return False
    
    def get_project_files(self, project_path: Union[str, Path], include_gitignore: bool = True) -> List[Path]:
        """
        Get project file list, supports .gitignore filtering
        
        Args:
            project_path: Project path
            include_gitignore: Whether to apply .gitignore filtering
            
        Returns:
            List of file paths
        """
        project_path = Path(project_path)
        
        if not project_path.exists():
            return []
        
        files = []
        gitignore_patterns = []
        
        # Read .gitignore file
        if include_gitignore:
            gitignore_path = project_path / ".gitignore"
            gitignore_patterns = self.parse_gitignore(gitignore_path)
        
        # Traverse project files
        for file_path in project_path.rglob("*"):
            if file_path.is_file():
                # If it's a text file and not ignored by .gitignore
                if self.is_text_file(file_path):
                    if not include_gitignore or not self.should_ignore_file(file_path, gitignore_patterns, project_path):
                        files.append(file_path)
        
        return files 