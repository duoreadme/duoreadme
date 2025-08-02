# 多语言 README 生成工具 CLI 使用指南

## 概述

这个项目提供了多个 CLI 工具来将项目代码和 README 翻译成多种语言并保存到 docs 目录。

## 可用的 CLI 工具

### 1. 一键运行脚本

最简单的使用方式，一键完成所有流程：

```bash
python run_translation.py
```

这个脚本会自动执行：
- 翻译项目内容
- 解析多语言 README
- 生成总结报告

### 2. 简化版 CLI

```bash
python simple_cli.py
```

功能：
- 读取 project 目录下的文件
- 调用翻译脚本
- 显示生成的文件列表

帮助信息：
```bash
python simple_cli.py --help
```

### 3. 完整版 CLI (功能最全)

```bash
python cli.py
```

支持的命令行参数：
```bash
# 使用默认设置
python cli.py

# 指定项目路径
python cli.py --project-path ./myproject

# 指定要翻译的语言
python cli.py --languages 中文 English 日本語

# 不保存原始响应
python cli.py --no-save-raw

# 显示版本信息
python cli.py --version
```

### 4. 单独运行各个脚本

如果需要单独运行某个步骤：

```bash
# 只运行翻译
python translate_readme.py

# 只运行解析
python parse_translation.py

# 只运行总结
python summary.py
```

## 生成的文件

运行完成后，会在 `docs` 目录下生成以下文件：

- `README.en.md` - English 版本
- `README.zh.md` - 中文版本
- `README.th.md` - 泰语版本
- `README_translation_response.txt` - 原始翻译响应

## 支持的语言

默认支持以下语言：
- 中文 (Chinese)
- English
- 日本語 (Japanese)
- 한국어 (Korean)
- Français (French)
- Deutsch (German)
- Español (Spanish)
- Italiano (Italian)
- Português (Portuguese)
- Русский (Russian)

## 项目结构要求

工具期望的项目结构：
```
project/
├── README.md
└── src/
    ├── compile.ts
    └── 其他文件...
```

## 环境要求

1. Python 3.6+
2. 安装依赖包：
   ```bash
   pip install -r requirements.txt
   ```

## 故障排除

### 1. distutils 错误

如果遇到 `_distutils_hack` 模块错误，可以尝试：

```bash
# 方法1: 使用简化版 CLI
python simple_cli.py

# 方法2: 单独运行脚本
python translate_readme.py
python parse_translation.py
python summary.py
```

### 2. 依赖包缺失

如果缺少依赖包：
```bash
pip install -r requirements.txt
```

### 3. 项目文件不存在

确保 `project` 目录存在且包含 `README.md` 和 `src` 目录。

## 示例输出

成功运行后的输出示例：
```
🚀 多语言 README 生成工具
==================================================
📖 步骤 1: 运行翻译脚本
✓ 已读取 project/README.md
✓ 已读取 project/src/compile.ts
项目内容读取完成
✓ 创建 docs 目录
正在发送翻译请求...
✅ 翻译完成
正在解析多语言 README...
未能解析到多语言 README 内容
已保存原始响应到 docs/README_translation_response.txt

🔍 步骤 2: 运行解析脚本
开始解析翻译响应...
找到 English 版本
找到 中文 版本
找到 ไทย 版本
已保存 English README 到 docs/README.en.md
已保存 中文 README 到 docs/README.zh.md
已保存 ไทย README 到 docs/README.th.md
成功解析并保存了 3 种语言的 README

📊 步骤 3: 运行总结脚本
============================================================
项目翻译和解析完成总结
============================================================
✓ docs 目录已创建
生成的文件:
  - README.en.md (1390 bytes)
  - README.th.md (2949 bytes)
  - README.zh.md (1283 bytes)
  - README_translation_response.txt (5698 bytes)
✓ 成功生成了 3 种语言的 README:
  - English
  - ไทย (泰语)
  - 中文
============================================================
任务完成！
============================================================

🎉 所有任务完成！
```

## 注意事项

1. 翻译过程需要网络连接
2. 翻译质量取决于 AI 服务的响应
3. 建议在翻译完成后检查生成的文件内容
4. 如果解析失败，可以手动查看 `README_translation_response.txt` 文件 