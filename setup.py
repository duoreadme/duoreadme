"""
DuoReadme Installation Configuration

Installation configuration file for the multilingual README generation tool.
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

# Read requirements.txt
requirements = []
if (this_directory / "requirements.txt").exists():
    with open(this_directory / "requirements.txt", "r", encoding="utf-8") as f:
        requirements = [line.strip() for line in f if line.strip() and not line.startswith("#")]

setup(
    name="duoreadme",
    version="1.0.0",
    author="DuoReadme Team",
    author_email="team@duoreadme.com",
    description="A powerful CLI tool for automatically generating project code and README into multiple languages and creating standardized multilingual documentation",
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