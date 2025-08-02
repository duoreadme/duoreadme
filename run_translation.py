#!/usr/bin/env python3
"""
多语言 README 生成工具 - 一键运行脚本
"""

import os
import sys
from pathlib import Path

def main():
    """主函数 - 一键运行所有流程"""
    print("🚀 多语言 README 生成工具")
    print("=" * 50)
    
    try:
        # 1. 运行翻译脚本
        print("\n📖 步骤 1: 运行翻译脚本")
        import translate_readme
        translate_readme.translate_project_content()
        
        # 2. 运行解析脚本
        print("\n🔍 步骤 2: 运行解析脚本")
        import parse_translation
        parse_translation.main()
        
        # 3. 运行总结脚本
        print("\n📊 步骤 3: 运行总结脚本")
        import summary
        summary.print_summary()
        
        print("\n🎉 所有任务完成！")
        
    except Exception as e:
        print(f"\n❌ 执行过程中出现错误: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 