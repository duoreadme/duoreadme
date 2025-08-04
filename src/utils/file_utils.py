"""
文件操作工具模块

提供文件读写和操作的工具函数。
"""

import os
import shutil
import fnmatch
from pathlib import Path
from typing import List, Optional, Union


class FileUtils:
    """文件操作工具类"""
    
    def read_text_file(self, file_path: Union[str, Path], encoding: str = "utf-8") -> str:
        """
        读取文本文件
        
        Args:
            file_path: 文件路径
            encoding: 文件编码
            
        Returns:
            文件内容
            
        Raises:
            FileNotFoundError: 文件不存在
            UnicodeDecodeError: 编码错误
        """
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"文件不存在: {file_path}")
        
        try:
            return file_path.read_text(encoding=encoding)
        except UnicodeDecodeError as e:
            raise UnicodeDecodeError(f"文件编码错误 {file_path}: {e}")
    
    def write_text_file(self, file_path: Union[str, Path], content: str, encoding: str = "utf-8"):
        """
        写入文本文件
        
        Args:
            file_path: 文件路径
            content: 要写入的内容
            encoding: 文件编码
            
        Raises:
            OSError: 写入失败
        """
        file_path = Path(file_path)
        
        # 确保目录存在
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            file_path.write_text(content, encoding=encoding)
        except OSError as e:
            raise OSError(f"写入文件失败 {file_path}: {e}")
    
    def read_binary_file(self, file_path: Union[str, Path]) -> bytes:
        """
        读取二进制文件
        
        Args:
            file_path: 文件路径
            
        Returns:
            文件内容
            
        Raises:
            FileNotFoundError: 文件不存在
        """
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"文件不存在: {file_path}")
        
        return file_path.read_bytes()
    
    def write_binary_file(self, file_path: Union[str, Path], content: bytes):
        """
        写入二进制文件
        
        Args:
            file_path: 文件路径
            content: 要写入的内容
            
        Raises:
            OSError: 写入失败
        """
        file_path = Path(file_path)
        
        # 确保目录存在
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            file_path.write_bytes(content)
        except OSError as e:
            raise OSError(f"写入文件失败 {file_path}: {e}")
    
    def copy_file(self, src: Union[str, Path], dst: Union[str, Path]):
        """
        复制文件
        
        Args:
            src: 源文件路径
            dst: 目标文件路径
            
        Raises:
            FileNotFoundError: 源文件不存在
            OSError: 复制失败
        """
        src = Path(src)
        dst = Path(dst)
        
        if not src.exists():
            raise FileNotFoundError(f"源文件不存在: {src}")
        
        # 确保目标目录存在
        dst.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            shutil.copy2(src, dst)
        except OSError as e:
            raise OSError(f"复制文件失败 {src} -> {dst}: {e}")
    
    def move_file(self, src: Union[str, Path], dst: Union[str, Path]):
        """
        移动文件
        
        Args:
            src: 源文件路径
            dst: 目标文件路径
            
        Raises:
            FileNotFoundError: 源文件不存在
            OSError: 移动失败
        """
        src = Path(src)
        dst = Path(dst)
        
        if not src.exists():
            raise FileNotFoundError(f"源文件不存在: {src}")
        
        # 确保目标目录存在
        dst.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            shutil.move(str(src), str(dst))
        except OSError as e:
            raise OSError(f"移动文件失败 {src} -> {dst}: {e}")
    
    def delete_file(self, file_path: Union[str, Path]):
        """
        删除文件
        
        Args:
            file_path: 文件路径
            
        Raises:
            FileNotFoundError: 文件不存在
            OSError: 删除失败
        """
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"文件不存在: {file_path}")
        
        try:
            file_path.unlink()
        except OSError as e:
            raise OSError(f"删除文件失败 {file_path}: {e}")
    
    def create_directory(self, dir_path: Union[str, Path], exist_ok: bool = True):
        """
        创建目录
        
        Args:
            dir_path: 目录路径
            exist_ok: 如果目录已存在是否不报错
            
        Raises:
            OSError: 创建失败
        """
        dir_path = Path(dir_path)
        
        try:
            dir_path.mkdir(parents=True, exist_ok=exist_ok)
        except OSError as e:
            raise OSError(f"创建目录失败 {dir_path}: {e}")
    
    def delete_directory(self, dir_path: Union[str, Path], recursive: bool = False):
        """
        删除目录
        
        Args:
            dir_path: 目录路径
            recursive: 是否递归删除
            
        Raises:
            FileNotFoundError: 目录不存在
            OSError: 删除失败
        """
        dir_path = Path(dir_path)
        
        if not dir_path.exists():
            raise FileNotFoundError(f"目录不存在: {dir_path}")
        
        try:
            if recursive:
                shutil.rmtree(dir_path)
            else:
                dir_path.rmdir()
        except OSError as e:
            raise OSError(f"删除目录失败 {dir_path}: {e}")
    
    def list_files(self, dir_path: Union[str, Path], pattern: str = "*", recursive: bool = False) -> List[Path]:
        """
        列出目录中的文件
        
        Args:
            dir_path: 目录路径
            pattern: 文件匹配模式
            recursive: 是否递归搜索
            
        Returns:
            文件路径列表
            
        Raises:
            FileNotFoundError: 目录不存在
        """
        dir_path = Path(dir_path)
        
        if not dir_path.exists():
            raise FileNotFoundError(f"目录不存在: {dir_path}")
        
        if not dir_path.is_dir():
            raise NotADirectoryError(f"不是目录: {dir_path}")
        
        if recursive:
            return list(dir_path.rglob(pattern))
        else:
            return list(dir_path.glob(pattern))
    
    def get_file_size(self, file_path: Union[str, Path]) -> int:
        """
        获取文件大小
        
        Args:
            file_path: 文件路径
            
        Returns:
            文件大小（字节）
            
        Raises:
            FileNotFoundError: 文件不存在
        """
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"文件不存在: {file_path}")
        
        return file_path.stat().st_size
    
    def get_file_info(self, file_path: Union[str, Path]) -> dict:
        """
        获取文件信息
        
        Args:
            file_path: 文件路径
            
        Returns:
            文件信息字典
            
        Raises:
            FileNotFoundError: 文件不存在
        """
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"文件不存在: {file_path}")
        
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
        确保目录存在，如果不存在则创建
        
        Args:
            dir_path: 目录路径
        """
        dir_path = Path(dir_path)
        dir_path.mkdir(parents=True, exist_ok=True)
    
    def is_text_file(self, file_path: Union[str, Path]) -> bool:
        """
        判断是否为文本文件
        
        Args:
            file_path: 文件路径
            
        Returns:
            是否为文本文件
        """
        file_path = Path(file_path)
        
        if not file_path.exists() or not file_path.is_file():
            return False
        
        # 检查文件扩展名
        text_extensions = {
            '.txt', '.md', '.py', '.js', '.ts', '.html', '.css', '.json', 
            '.xml', '.yaml', '.yml', '.ini', '.cfg', '.conf', '.log'
        }
        
        if file_path.suffix.lower() in text_extensions:
            return True
        
        # 尝试读取文件开头判断是否为文本
        try:
            with open(file_path, 'rb') as f:
                chunk = f.read(1024)
                return chunk.decode('utf-8', errors='ignore').isprintable()
        except:
            return False
    
    def parse_gitignore(self, gitignore_path: Union[str, Path]) -> List[str]:
        """
        解析 .gitignore 文件
        
        Args:
            gitignore_path: .gitignore 文件路径
            
        Returns:
            忽略模式列表
        """
        gitignore_path = Path(gitignore_path)
        patterns = []
        
        if not gitignore_path.exists():
            return patterns
        
        try:
            with open(gitignore_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    # 跳过空行和注释
                    if line and not line.startswith('#'):
                        patterns.append(line)
        except Exception as e:
            print(f"警告: 读取 .gitignore 文件失败: {e}")
        
        return patterns
    
    def should_ignore_file(self, file_path: Union[str, Path], gitignore_patterns: List[str], base_path: Union[str, Path]) -> bool:
        """
        判断文件是否应该被忽略
        
        Args:
            file_path: 文件路径
            gitignore_patterns: .gitignore 模式列表
            base_path: 基础路径（.gitignore 文件所在目录）
            
        Returns:
            是否应该忽略
        """
        file_path = Path(file_path)
        base_path = Path(base_path)
        
        # 计算相对于基础路径的相对路径
        try:
            relative_path = file_path.relative_to(base_path)
        except ValueError:
            # 如果文件不在基础路径下，不忽略
            return False
        
        # 转换为字符串，使用正斜杠分隔符（gitignore 标准）
        relative_path_str = str(relative_path).replace('\\', '/')
        
        for pattern in gitignore_patterns:
            # 处理目录模式（以 / 结尾）
            if pattern.endswith('/'):
                if relative_path_str.startswith(pattern[:-1]) or fnmatch.fnmatch(relative_path_str, pattern[:-1]):
                    return True
            
            # 处理文件模式
            if fnmatch.fnmatch(relative_path_str, pattern):
                return True
            
            # 处理通配符模式
            if fnmatch.fnmatch(relative_path_str, pattern):
                return True
        
        return False
    
    def get_project_files(self, project_path: Union[str, Path], include_gitignore: bool = True) -> List[Path]:
        """
        获取项目文件列表，支持 .gitignore 过滤
        
        Args:
            project_path: 项目路径
            include_gitignore: 是否应用 .gitignore 过滤
            
        Returns:
            文件路径列表
        """
        project_path = Path(project_path)
        
        if not project_path.exists():
            return []
        
        files = []
        gitignore_patterns = []
        
        # 读取 .gitignore 文件
        if include_gitignore:
            gitignore_path = project_path / ".gitignore"
            gitignore_patterns = self.parse_gitignore(gitignore_path)
        
        # 遍历项目文件
        for file_path in project_path.rglob("*"):
            if file_path.is_file():
                # 如果是文本文件且不被 .gitignore 忽略
                if self.is_text_file(file_path):
                    if not include_gitignore or not self.should_ignore_file(file_path, gitignore_patterns, project_path):
                        files.append(file_path)
        
        return files 