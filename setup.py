"""
DuoReadme 安装配置

多语言 README 生成工具的安装配置文件。
"""

from setuptools import setup, find_packages
from pathlib import Path

# 读取README文件
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

# 读取requirements.txt
requirements = []
if (this_directory / "requirements.txt").exists():
    with open(this_directory / "requirements.txt", "r", encoding="utf-8") as f:
        requirements = [line.strip() for line in f if line.strip() and not line.startswith("#")]

setup(
    name="duoreadme",
    version="1.0.0",
    author="DuoReadme Team",
    author_email="team@duoreadme.com",
    description="一个强大的CLI工具，用于将项目代码和README自动生成多种语言并生成规范化的多语言文档",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/your-username/duoreadme",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Documentation",
        "Topic :: Software Development :: Documentation",
        "Topic :: Text Processing :: Linguistic",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=21.0",
            "flake8>=3.8",
            "mypy>=0.800",
        ],
        "cli": [
            "click>=8.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "duoreadme=src.cli.main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.md", "*.txt", "*.yaml", "*.yml"],
    },
    keywords="readme translation multilingual documentation cli",
    project_urls={
        "Bug Reports": "https://github.com/your-username/duoreadme/issues",
        "Source": "https://github.com/your-username/duoreadme",
        "Documentation": "https://github.com/your-username/duoreadme/wiki",
    },
) 