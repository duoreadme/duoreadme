# DuoReadme - 多语言 README 生成工具

一个强大的CLI工具，用于将项目代码和README自动翻译成多种语言并生成规范化的多语言文档。

## 🚀 功能特性

- **多语言支持**: 支持10种主流语言（中文、英文、日文、韩文、法文、德文、西班牙文、意大利文、葡萄牙文、俄文）
- **智能解析**: 自动解析项目结构和代码内容
- **批量处理**: 一键生成所有语言的README文档
- **腾讯云集成**: 集成腾讯云翻译服务
- **灵活配置**: 支持自定义项目路径和语言选择

## 📁 项目结构

```
duoreadme/
├── README.md                 # 项目主文档
├── requirements.txt          # Python依赖包
├── setup.py                 # 安装配置
├── pyproject.toml           # 项目配置
├── .gitignore              # Git忽略文件
├── docs/                   # 生成的文档目录
├── src/                    # 源代码目录
│   ├── __init__.py
│   ├── core/               # 核心功能模块
│   │   ├── __init__.py
│   │   ├── translator.py   # 翻译核心逻辑
│   │   ├── parser.py       # 内容解析器
│   │   └── generator.py    # 文档生成器
│   ├── cli/                # CLI工具模块
│   │   ├── __init__.py
│   │   ├── main.py         # 主CLI入口
│   │   └── commands.py     # CLI命令
│   ├── services/           # 外部服务集成
│   │   ├── __init__.py
│   │   ├── tencent_cloud.py # 腾讯云服务
│   │   └── sse_client.py   # SSE客户端
│   ├── utils/              # 工具函数
│   │   ├── __init__.py
│   │   ├── file_utils.py   # 文件操作工具
│   │   └── config.py       # 配置管理
│   └── models/             # 数据模型
│       ├── __init__.py
│       └── types.py        # 类型定义
├── tests/                  # 测试目录
│   ├── __init__.py
│   ├── test_translator.py
│   ├── test_parser.py
│   └── test_cli.py
├── examples/               # 示例目录
│   ├── sample_project/     # 示例项目
│   └── usage_examples.py   # 使用示例
└── scripts/                # 脚本目录
    ├── install.sh          # 安装脚本
    └── run_tests.sh        # 测试脚本
```

## 🛠️ 安装

```bash
# 克隆项目
git clone https://github.com/your-username/duoreadme.git
cd duoreadme

# 安装依赖
pip install -r requirements.txt

# 安装项目
pip install -e .
```

## 📖 使用方法

### 基本使用

```bash
# 查看所有可用命令
python -m src.cli.main --help

# 翻译项目并生成多语言README（自动应用 .gitignore 过滤）
python -m src.cli.main translate

# 指定项目路径翻译
python -m src.cli.main translate --project-path ./myproject

# 指定要翻译的语言
python -m src.cli.main translate --languages "zh,en,ja"
```

### 可用命令

#### translate - 翻译项目
```bash
# 使用默认设置翻译项目
python -m src.cli.main translate

# 指定项目路径
python -m src.cli.main translate --project-path ./myproject

# 指定要翻译的语言
python -m src.cli.main translate --languages "zh,en,ja"

# 指定输出目录
python -m src.cli.main translate --output-dir ./my_docs

# 不保存原始响应
python -m src.cli.main translate --no-save-raw

# 显示详细输出
python -m src.cli.main translate --verbose
```

**📝 关于 .gitignore 支持**

翻译器会自动检测项目根目录下的 `.gitignore` 文件，并过滤掉被忽略的文件和目录。这确保只翻译项目中真正重要的源代码文件，避免处理临时文件、构建产物、依赖包等。

- ✅ 如果项目有 `.gitignore` 文件，会自动应用过滤规则
- ✅ 如果没有 `.gitignore` 文件，会读取所有文本文件
- ✅ 支持标准的 `.gitignore` 语法（通配符、目录模式等）
- ✅ 优先读取 `README.md` 文件，然后读取其他源代码文件



#### config - 显示配置信息
```bash
# 显示当前配置
python -m src.cli.main config

# 显示指定配置文件
python -m src.cli.main config --config ./my_config.yaml
```

#### list - 列出已生成的文件
```bash
# 列出默认输出目录的文件
python -m src.cli.main list

# 列出指定输出目录的文件
python -m src.cli.main list --output-dir ./my_docs
```

### 全局选项

```bash
# 显示版本信息
python -m src.cli.main --version

# 显示帮助信息
python -m src.cli.main --help
```

### 编程接口

```python
from src.core.translator import Translator
from src.core.parser import Parser

# 创建翻译器
translator = Translator()

# 翻译项目内容
result = translator.translate_project("./sample_project")

# 解析多语言内容
parser = Parser()
readme_dict = parser.parse_multilingual_content(result)
```

## 🔧 配置

### 环境变量

```bash
# 腾讯云配置
export TENCENTCLOUD_SECRET_ID="your_secret_id"
export TENCENTCLOUD_SECRET_KEY="your_secret_key"
# 应用配置
export DUOREADME_BOT_APP_KEY="your_bot_app_key"
```

### 配置文件

创建 `config.yaml` 文件：

```yaml
# 腾讯云配置
tencent_cloud:
  secret_id: "your_secret_id"
  secret_key: "your_secret_key"
  region: "ap-beijing"

# 翻译配置
translation:
  default_languages:
    - "中文"
    - "English"
    - "日本語"
  batch_size: 5
  timeout: 30


```

## 🧪 测试

```bash
# 运行所有测试
python -m pytest tests/

# 运行特定测试
python -m pytest tests/test_translator.py
```

## 📝 示例

### 示例项目结构

```
sample_project/
├── README.md
└── src/
    ├── main.py
    └── utils.py
```

### 运行示例

```bash
# 翻译示例项目
python -m src.cli.main translate --project-path examples/sample_project

# 查看生成的文件
ls docs/
# README.zh.md
# README.en.md
# README.ja.md
```