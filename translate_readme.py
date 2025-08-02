import sseclient
import requests
import json
import session
import os
import re

bot_app_key = "iIuhxDngAPmYRviQivBhDWVjxupvbeahuYivbmljFcNIyfHRcJdqLjjFTqYjwkBsuyhQMICCAbuEIfKzbhRelPxPZroXYEHzVoHpnuwcPnxErHdmzPGSUDCIiwkVtPkc"
visitor_biz_id = "202403130001"
streaming_throttle = 1

def read_project_files():
    """读取项目文件内容"""
    content = ""
    
    # 读取 README.md
    try:
        with open("project/README.md", "r", encoding="utf-8") as f:
            content += "=== README.md ===\n"
            content += f.read()
            content += "\n\n"
    except Exception as e:
        print(f"读取 README.md 失败: {e}")
    
    # 读取 src/compile.ts
    try:
        with open("project/src/compile.ts", "r", encoding="utf-8") as f:
            content += "=== src/compile.ts ===\n"
            content += f.read()
            content += "\n\n"
    except Exception as e:
        print(f"读取 compile.ts 失败: {e}")
    
    return content

def create_docs_directory():
    """创建 docs 目录"""
    if not os.path.exists("docs"):
        os.makedirs("docs")
        print("创建 docs 目录")

def parse_multilingual_readme(response_text):
    """解析多语言 README 内容"""
    # 查找不同语言的 README 部分
    languages = {
        "中文": r"### 中文\s*\n(.*?)(?=\n### |$)",
        "English": r"### English\s*\n(.*?)(?=\n### |$)",
        "日本語": r"### 日本語\s*\n(.*?)(?=\n### |$)",
        "한국어": r"### 한국어\s*\n(.*?)(?=\n### |$)",
        "Français": r"### Français\s*\n(.*?)(?=\n### |$)",
        "Deutsch": r"### Deutsch\s*\n(.*?)(?=\n### |$)",
        "Español": r"### Español\s*\n(.*?)(?=\n### |$)",
        "Italiano": r"### Italiano\s*\n(.*?)(?=\n### |$)",
        "Português": r"### Português\s*\n(.*?)(?=\n### |$)",
        "Русский": r"### Русский\s*\n(.*?)(?=\n### |$)"
    }
    
    results = {}
    for lang, pattern in languages.items():
        match = re.search(pattern, response_text, re.DOTALL)
        if match:
            content = match.group(1).strip()
            if content:
                results[lang] = content
    
    return results

def save_readme_files(readme_dict):
    """保存多语言 README 文件"""
    for lang, content in readme_dict.items():
        # 创建文件名
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
        
        filename = filename_map.get(lang, f"README.{lang.lower()}.md")
        filepath = os.path.join("docs", filename)
        
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"已保存 {lang} README 到 {filepath}")
        except Exception as e:
            print(f"保存 {lang} README 失败: {e}")

def translate_project_content():
    """翻译项目内容"""
    # 读取项目文件
    project_content = read_project_files()
    print("项目内容读取完成")
    
    # 创建 docs 目录
    create_docs_directory()
    
    # 构建请求内容
    prompt = f"""请将以下项目代码和README翻译成多种语言的README文档，包括中文、English、日本語、한국어、Français、Deutsch、Español、Italiano、Português、Русский。

项目内容：
{project_content}

请为每种语言生成完整的README文档，包含项目介绍、功能说明、使用方法等。格式如下：

### 中文
[中文README内容]

### English  
[English README content]

### 日本語
[日本語README内容]

### 한국어
[한국어README 내용]

### Français
[Contenu README français]

### Deutsch
[Deutscher README-Inhalt]

### Español
[Contenido README en español]

### Italiano
[Contenuto README italiano]

### Português
[Conteúdo README em português]

### Русский
[Содержание README на русском]
"""
    
    # 发送 SSE 请求
    req_data = {
        "content": prompt,
        "bot_app_key": bot_app_key,
        "visitor_biz_id": visitor_biz_id,
        "session_id": session.get_session(),
        "streaming_throttle": streaming_throttle
    }
    
    try:
        print("正在发送翻译请求...")
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
                    print(f'发送内容: {data["payload"]["content"]}')
                elif data["payload"]["is_final"]:
                    print("翻译完成")
                    full_response = data["payload"]["content"]
                    break
                else:
                    print(f'接收中: {data["payload"]["content"]}')
                    full_response += data["payload"]["content"]
        
        # 解析多语言 README
        print("正在解析多语言 README...")
        readme_dict = parse_multilingual_readme(full_response)
        
        if readme_dict:
            # 保存文件
            save_readme_files(readme_dict)
            print(f"成功解析并保存了 {len(readme_dict)} 种语言的 README")
        else:
            print("未能解析到多语言 README 内容")
            # 保存原始响应作为备用
            with open("docs/README_translation_response.txt", "w", encoding="utf-8") as f:
                f.write(full_response)
            print("已保存原始响应到 docs/README_translation_response.txt")
            
    except Exception as e:
        print(f"翻译过程中出现错误: {e}")

if __name__ == "__main__":
    translate_project_content() 