import os

def print_summary():
    """打印翻译和解析过程的总结"""
    print("=" * 60)
    print("项目翻译和解析完成总结")
    print("=" * 60)
    
    # 检查 docs 目录
    if os.path.exists("docs"):
        print(f"✓ docs 目录已创建")
        
        # 列出生成的文件
        files = os.listdir("docs")
        print(f"\n生成的文件:")
        for file in sorted(files):
            filepath = os.path.join("docs", file)
            size = os.path.getsize(filepath)
            print(f"  - {file} ({size} bytes)")
        
        # 统计语言版本
        language_files = [f for f in files if f.startswith("README.") and f.endswith(".md")]
        print(f"\n✓ 成功生成了 {len(language_files)} 种语言的 README:")
        
        language_map = {
            "README.en.md": "English",
            "README.zh.md": "中文", 
            "README.th.md": "ไทย (泰语)"
        }
        
        for file in sorted(language_files):
            lang_name = language_map.get(file, file)
            print(f"  - {lang_name}")
            
    else:
        print("✗ docs 目录不存在")
    
    print("\n" + "=" * 60)
    print("任务完成！")
    print("=" * 60)

if __name__ == "__main__":
    print_summary() 