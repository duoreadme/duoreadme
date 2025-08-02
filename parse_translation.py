import re
import os

def parse_translation_response():
    """解析翻译响应文件并提取多语言README"""
    
    # 读取响应文件
    with open("docs/README_translation_response.txt", "r", encoding="utf-8") as f:
        content = f.read()
    
    # 定义语言模式
    language_patterns = {
        "English": r"英文版本readme:\s*\n(.*?)(?=\n---\n|$)",
        "中文": r"中文版本readme：\s*\n(.*?)(?=\n---\n|$)",
        "ไทย": r"泰语版本readme:\s*\n(.*?)(?=\n---\n|$)"
    }
    
    results = {}
    
    for lang, pattern in language_patterns.items():
        match = re.search(pattern, content, re.DOTALL)
        if match:
            content_text = match.group(1).strip()
            if content_text:
                results[lang] = content_text
                print(f"找到 {lang} 版本")
    
    return results

def save_readme_files(readme_dict):
    """保存多语言 README 文件"""
    filename_map = {
        "English": "README.en.md",
        "中文": "README.zh.md",
        "ไทย": "README.th.md"
    }
    
    for lang, content in readme_dict.items():
        filename = filename_map.get(lang, f"README.{lang.lower()}.md")
        filepath = os.path.join("docs", filename)
        
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"已保存 {lang} README 到 {filepath}")
        except Exception as e:
            print(f"保存 {lang} README 失败: {e}")

def main():
    print("开始解析翻译响应...")
    
    # 解析响应
    readme_dict = parse_translation_response()
    
    if readme_dict:
        # 保存文件
        save_readme_files(readme_dict)
        print(f"成功解析并保存了 {len(readme_dict)} 种语言的 README")
        
        # 显示找到的语言
        print("\n找到的语言版本:")
        for lang in readme_dict.keys():
            print(f"- {lang}")
    else:
        print("未能解析到多语言 README 内容")

if __name__ == "__main__":
    main() 