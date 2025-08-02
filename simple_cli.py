#!/usr/bin/env python3
"""
简化版多语言 README 生成 CLI 工具
用于将项目代码和 README 翻译成多种语言并保存到 docs 目录
"""

import os
import sys
import json
import re
from pathlib import Path

def read_project_files(project_path="project"):
    """读取项目文件内容"""
    content = ""
    project_path = Path(project_path)
    
    # 读取 README.md
    readme_path = project_path / "README.md"
    if readme_path.exists():
        try:
            with open(readme_path, "r", encoding="utf-8") as f:
                content += "=== README.md ===\n"
                content += f.read()
                content += "\n\n"
            print(f"✓ 已读取 {readme_path}")
        except Exception as e:
            print(f"✗ 读取 README.md 失败: {e}")
    else:
        print(f"⚠ 未找到 {readme_path}")
    
    # 读取 src 目录下的所有文件
    src_path = project_path / "src"
    if src_path.exists():
        for file_path in src_path.rglob("*"):
            if file_path.is_file():
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content += f"=== {file_path.relative_to(project_path)} ===\n"
                        content += f.read()
                        content += "\n\n"
                    print(f"✓ 已读取 {file_path.relative_to(project_path)}")
                except Exception as e:
                    print(f"✗ 读取 {file_path} 失败: {e}")
    else:
        print(f"⚠ 未找到 {src_path}")
    
    return content

def create_docs_directory():
    """创建 docs 目录"""
    docs_path = Path("docs")
    if not docs_path.exists():
        docs_path.mkdir()
        print("✓ 创建 docs 目录")
    else:
        print("✓ docs 目录已存在")

def run_translation_workflow():
    """运行翻译工作流程"""
    print("🚀 开始多语言 README 生成流程")
    print("="*60)
    
    # 1. 读取项目文件
    print("\n📖 步骤 1: 读取项目文件")
    project_content = read_project_files("project")
    if not project_content.strip():
        print("❌ 未找到任何项目内容")
        return False
    
    # 2. 创建 docs 目录
    print("\n📁 步骤 2: 创建输出目录")
    create_docs_directory()
    
    # 3. 调用现有的翻译脚本
    print("\n🌐 步骤 3: 调用翻译脚本")
    try:
        # 导入并运行翻译脚本
        import translate_readme
        translate_readme.translate_project_content()
        print("✅ 翻译完成")
        return True
    except Exception as e:
        print(f"❌ 翻译失败: {e}")
        return False

def show_help():
    """显示帮助信息"""
    help_text = """
多语言 README 生成工具

用法:
  python simple_cli.py          # 运行完整的翻译流程
  python simple_cli.py --help   # 显示帮助信息

功能:
  - 读取 project 目录下的 README.md 和 src 文件
  - 通过 SSE 发送翻译请求
  - 解析多语言 README 内容
  - 保存到 docs 目录

生成的文件:
  - README.en.md (English)
  - README.zh.md (中文)
  - README.th.md (泰语)
  - README_translation_response.txt (原始响应)

示例:
  python simple_cli.py
    """
    print(help_text)

def main():
    """主函数"""
    if len(sys.argv) > 1:
        if sys.argv[1] in ["--help", "-h", "help"]:
            show_help()
            return
    
    # 运行翻译流程
    success = run_translation_workflow()
    
    if success:
        print("\n🎯 所有任务已完成！")
        print("\n📁 生成的文件:")
        docs_path = Path("docs")
        if docs_path.exists():
            for file_path in sorted(docs_path.glob("*")):
                size = file_path.stat().st_size
                print(f"  - {file_path.name} ({size} bytes)")
    else:
        print("\n💥 任务执行失败！")
        sys.exit(1)

if __name__ == "__main__":
    main() 