#!/usr/bin/env python3
"""
多语言 README 生成 CLI 工具
用于将项目代码和 README 翻译成多种语言并保存到 docs 目录
"""

import argparse
import os
import sys
import json
import re
from pathlib import Path

# 导入现有的模块
try:
    import sseclient
    import requests
    import session
except ImportError as e:
    print(f"错误: 缺少必要的依赖包 - {e}")
    print("请运行: pip install -r requirements.txt")
    sys.exit(1)

class MultilingualReadmeGenerator:
    def __init__(self):
        self.bot_app_key = "iIuhxDngAPmYRviQivBhDWVjxupvbeahuYivbmljFcNIyfHRcJdqLjjFTqYjwkBsuyhQMICCAbuEIfKzbhRelPxPZroXYEHzVoHpnuwcPnxErHdmzPGSUDCIiwkVtPkc"
        self.visitor_biz_id = "202403130001"
        self.streaming_throttle = 1
        
    def read_project_files(self, project_path="project"):
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
    
    def create_docs_directory(self):
        """创建 docs 目录"""
        docs_path = Path("docs")
        if not docs_path.exists():
            docs_path.mkdir()
            print("✓ 创建 docs 目录")
        else:
            print("✓ docs 目录已存在")
    
    def translate_content(self, project_content, languages=None):
        """翻译项目内容"""
        if languages is None:
            languages = ["中文", "English", "日本語", "한국어", "Français", "Deutsch", "Español", "Italiano", "Português", "Русский"]
        
        # 构建语言列表字符串
        languages_str = "、".join(languages)
        
        prompt = f"""请将以下项目代码和README翻译成多种语言的README文档，包括{languages_str}。

项目内容：
{project_content}

请为每种语言生成完整的README文档，包含项目介绍、功能说明、使用方法等。格式如下：

"""
        
        # 为每种语言添加格式说明
        for lang in languages:
            prompt += f"### {lang}\n[{lang}README内容]\n\n"
        
        # 发送 SSE 请求
        req_data = {
            "content": prompt,
            "bot_app_key": self.bot_app_key,
            "visitor_biz_id": self.visitor_biz_id,
            "session_id": session.get_session(),
            "streaming_throttle": self.streaming_throttle
        }
        
        try:
            print("🔄 正在发送翻译请求...")
            resp = requests.post(
                "https://wss.lke.cloud.tencent.com/v1/qbot/chat/sse", 
                data=json.dumps(req_data),
                stream=True, 
                headers={"Accept": "text/event-stream"}
            )
            
            client = sseclient.SSEClient(resp)
            full_response = ""
            
            for ev in client.events():
                data = json.loads(ev.data)
                if ev.event == "reply":
                    if data["payload"]["is_from_self"]:
                        print(f'📤 发送内容: {data["payload"]["content"][:50]}...')
                    elif data["payload"]["is_final"]:
                        print("✅ 翻译完成")
                        full_response = data["payload"]["content"]
                        break
                    else:
                        print(f'📥 接收中...', end='\r')
                        full_response += data["payload"]["content"]
            
            return full_response
            
        except Exception as e:
            print(f"❌ 翻译过程中出现错误: {e}")
            return None
    
    def parse_multilingual_readme(self, response_text, languages=None):
        """解析多语言 README 内容"""
        if languages is None:
            languages = ["中文", "English", "日本語", "한국어", "Français", "Deutsch", "Español", "Italiano", "Português", "Русский"]
        
        results = {}
        
        for lang in languages:
            # 尝试多种可能的模式
            patterns = [
                rf"### {re.escape(lang)}\s*\n(.*?)(?=\n### |$)",
                rf"{lang}版本readme:\s*\n(.*?)(?=\n---\n|$)",
                rf"{lang}版本readme：\s*\n(.*?)(?=\n---\n|$)"
            ]
            
            for pattern in patterns:
                match = re.search(pattern, response_text, re.DOTALL)
                if match:
                    content = match.group(1).strip()
                    if content:
                        results[lang] = content
                        print(f"✓ 找到 {lang} 版本")
                        break
        
        return results
    
    def save_readme_files(self, readme_dict):
        """保存多语言 README 文件"""
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
        
        saved_files = []
        for lang, content in readme_dict.items():
            filename = filename_map.get(lang, f"README.{lang.lower()}.md")
            filepath = Path("docs") / filename
            
            try:
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(content)
                print(f"✓ 已保存 {lang} README 到 {filepath}")
                saved_files.append((lang, filepath))
            except Exception as e:
                print(f"❌ 保存 {lang} README 失败: {e}")
        
        return saved_files
    
    def generate_summary(self, saved_files):
        """生成总结报告"""
        print("\n" + "="*60)
        print("📋 项目翻译和解析完成总结")
        print("="*60)
        
        docs_path = Path("docs")
        if docs_path.exists():
            print(f"✓ docs 目录已创建")
            
            # 列出生成的文件
            files = list(docs_path.glob("*"))
            print(f"\n📁 生成的文件:")
            for file_path in sorted(files):
                size = file_path.stat().st_size
                print(f"  - {file_path.name} ({size} bytes)")
            
            # 统计语言版本
            language_files = [f for f in files if f.name.startswith("README.") and f.name.endswith(".md")]
            print(f"\n✅ 成功生成了 {len(language_files)} 种语言的 README:")
            
            for file_path in sorted(language_files):
                lang_name = file_path.stem.replace("README.", "")
                print(f"  - {lang_name}")
                
        else:
            print("❌ docs 目录不存在")
        
        print("\n" + "="*60)
        print("🎉 任务完成！")
        print("="*60)
    
    def run(self, project_path="project", languages=None, save_raw=True):
        """运行完整的翻译流程"""
        print("🚀 开始多语言 README 生成流程")
        print("="*60)
        
        # 1. 读取项目文件
        print("\n📖 步骤 1: 读取项目文件")
        project_content = self.read_project_files(project_path)
        if not project_content.strip():
            print("❌ 未找到任何项目内容")
            return False
        
        # 2. 创建 docs 目录
        print("\n📁 步骤 2: 创建输出目录")
        self.create_docs_directory()
        
        # 3. 翻译内容
        print("\n🌐 步骤 3: 翻译项目内容")
        response = self.translate_content(project_content, languages)
        if not response:
            print("❌ 翻译失败")
            return False
        
        # 4. 保存原始响应
        if save_raw:
            raw_file = Path("docs") / "README_translation_response.txt"
            try:
                with open(raw_file, "w", encoding="utf-8") as f:
                    f.write(response)
                print(f"✓ 已保存原始响应到 {raw_file}")
            except Exception as e:
                print(f"⚠ 保存原始响应失败: {e}")
        
        # 5. 解析多语言内容
        print("\n🔍 步骤 4: 解析多语言 README")
        readme_dict = self.parse_multilingual_readme(response, languages)
        
        if not readme_dict:
            print("❌ 未能解析到多语言 README 内容")
            return False
        
        # 6. 保存文件
        print("\n💾 步骤 5: 保存多语言 README")
        saved_files = self.save_readme_files(readme_dict)
        
        # 7. 生成总结
        print("\n📊 步骤 6: 生成总结报告")
        self.generate_summary(saved_files)
        
        return True

def main():
    parser = argparse.ArgumentParser(
        description="多语言 README 生成工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法:
  python cli.py                           # 使用默认设置
  python cli.py --project-path ./myproject  # 指定项目路径
  python cli.py --languages 中文 English    # 指定语言
  python cli.py --no-save-raw             # 不保存原始响应
        """
    )
    
    parser.add_argument(
        "--project-path", 
        default="project",
        help="项目路径 (默认: project)"
    )
    
    parser.add_argument(
        "--languages", 
        nargs="+",
        default=["中文", "English", "日本語", "한국어", "Français", "Deutsch", "Español", "Italiano", "Português", "Русский"],
        help="要翻译的语言列表"
    )
    
    parser.add_argument(
        "--no-save-raw",
        action="store_true",
        help="不保存原始翻译响应"
    )
    
    parser.add_argument(
        "--version",
        action="version",
        version="多语言 README 生成工具 v1.0.0"
    )
    
    args = parser.parse_args()
    
    # 创建生成器实例
    generator = MultilingualReadmeGenerator()
    
    # 运行翻译流程
    success = generator.run(
        project_path=args.project_path,
        languages=args.languages,
        save_raw=not args.no_save_raw
    )
    
    if success:
        print("\n🎯 所有任务已完成！")
        sys.exit(0)
    else:
        print("\n💥 任务执行失败！")
        sys.exit(1)

if __name__ == "__main__":
    main() 