# DuoReadme - 多语言 README 生成工具

DuoReadme 是一个强大的命令行工具，可以自动将项目代码和 README 翻译成多种语言，并生成标准化的多语言文档。

## 功能

- **多语言支持**：支持 100 多种语言，包括中文、英语、日语、韩语、法语、德语、西班牙语、意大利语、葡萄牙语、俄语等。完整的语言列表请参见 [ISO 语言代码](./LANGUAGE.md)。
- **智能解析**：自动解析项目结构和代码内容。
  1. 如果项目有一个 `.gitignore` 文件，它会自动应用过滤规则。
  2. DuoReadme 采用智能项目内容阅读策略，确保翻译的内容既全面又准确，基于文件和文件夹的级别。
- **批量处理**：一键生成所有语言的 README 文档。
- **腾讯云集成**：与腾讯云智能平台集成。
- **标准配置**：使用常见的项目标准，将英文 README.md 放在根目录中，其他语言的 README.md 文件放在 docs 目录中。
- **GitHub Actions 集成**：使用 GitHub Actions 自动将 README 文件翻译成多种语言。您可以参考 [GitHub Actions 集成](#github-actions-integration) 部分获取更多详细信息。

## 安装

```bash
pip install duoreadme
```

## 配置

> 您可以查看 [APPLY.md](./APPLY.md) 文件获取更多详细信息。

您可以查看 [config.yaml.example](./config.yaml.example) 文件获取配置文件。

## 使用

### gen - 生成多语言 README（使用高星 README 模板优化）

```bash
# 使用默认设置生成多语言 README
duoreadme gen

# 指定要翻译的语言
duoreadme gen --languages "zh-Hans,en,ja,ko,fr"

# 总体选项
Usage: duoreadme gen [OPTIONS]

  生成多语言 README

Options:
  --project-path TEXT  项目路径，默认为当前目录
  --languages TEXT     要生成的语言，逗号分隔，例如：zh-Hans,en,ja
  --config TEXT        配置文件路径
  --verbose            显示详细输出
  --debug              启用调试模式，输出 DEBUG 级别日志
  --help               显示此消息并退出
```

### trans - 仅文本翻译

`trans` 命令是一个纯文本翻译功能，从项目根目录读取 README 文件并将其翻译成多种语言。与处理整个项目结构的 `gen` 命令不同，`trans` 专注于翻译 README 内容。

```bash
# 使用默认设置翻译 README 文件
duoreadme trans

# 指定要翻译的语言
duoreadme trans --languages "zh-Hans,en,ja,ko,fr"

# 总体选项
Usage: duoreadme trans [OPTIONS]

  纯文本翻译功能 - 翻译项目根目录中的 README 文件

Options:
  --project-path TEXT  项目路径，默认为当前目录
  --languages TEXT     要翻译的语言，逗号分隔，例如：zh-
                       Hans,en,ja
  --config TEXT        配置文件路径
  --verbose            显示详细输出
  --debug              启用调试模式，输出 DEBUG 级别日志
  --help               显示此消息并退出
```

### config - 显示配置信息
```bash
# 显示当前内置配置
duoreadme config

# 启用调试模式以查看详细的配置信息
duoreadme config --debug
```

### set - 更新内置配置（仅限开发）
```bash
# 将新配置应用于内置配置（仅用于开发/构建）
duoreadme set my_config.yaml
```

### export - 导出内置配置
```bash
# 导出现有的内置配置
duoreadme export [-o exported_config.yaml]
```

## 编程接口

DuoReadme 提供了一个全面的 Python API，用于将翻译功能集成到您的应用程序中。

```python
from src.core.translator import Translator
from src.core.parser import Parser
from src.utils.config import Config

# 自定义配置
config = Config("custom_config.yaml")

# 使用自定义设置创建翻译器
translator = Translator(config)

# 使用特定语言进行翻译
languages = ["zh-Hans", "en", "ja", "ko"]
result = translator.translate_project(
    project_path="./my_project",
    languages=languages
)

# 解析和处理结果
parser = Parser()
parsed_content = parser.parse_multilingual_content(result)

# 访问翻译后的内容
for lang, content in parsed_content.content.items():
    print(f"Language: {lang}")
    print(f"Content: {content[:200]}...")
    print("-" * 50)
```

## GitHub Actions 集成

DuoReadme 可以通过 GitHub Actions 集成到您的 GitHub 存储库中，用于自动化翻译工作流程。

### 快速设置

> 您可以查看 [APPLY.md](./APPLY.md) 文件获取更多详细信息。

1. **配置密钥**：
   1. TENCENTCLOUD_SECRET_ID：在 [腾讯云控制台](https://console.cloud.tencent.com/cam/capi) 申请，选择 `新建密钥`。
   2. TENCENTCLOUD_SECRET_KEY：同上。
   3. DUOREADME_BOT_APP_KEY：在您的 [应用页面](https://lke.cloud.tencent.com/lke#/)，选择 `调用` 然后在 `appkey` 中找到它。
   4. GH_TOKEN：您可以在 `设置` - `开发者设置` - `个人访问令牌` - `令牌（经典）` - `生成新令牌` - `无过期` - `选择：repo 和 workflow` 中申请 GH_TOKEN。
   5. 将所需的密钥添加到您的存储库 `您的存储库` - `设置` - `安全性和变量` - `操作` - `新的存储库密钥`。

2. **使用操作**：将下面的操作文件添加到您的工作流文件夹 `.github/workflows/duoreadme.yml`。

```yaml
# .github/workflows/duoreadme.yml
name: DuoReadme

on:
  push: # 您可以更改触发条件。
    branches: [ main ]
    paths: [ 'README.md', 'docs/**' ]
  workflow_dispatch:

permissions:
  contents: write
  pull-requests: write

jobs:
  translate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          token: ${{ secrets.GH_TOKEN }}

      - name: Translate with custom settings
        uses: duoreadme/duoreadme@v0.1.2
        with:
          languages: "zh-Hans,en,ja" # 您可以指定多种语言，用逗号分隔
          translation_mode: "trans" # 您可以使用 'gen' 或 'trans' 选项。
          commit_message: "Update multilingual documentation" # 您可以自定义提交消息。
          debug: "false" # 您可以启用调试模式以查看详细日志。
        env:
          TENCENTCLOUD_SECRET_ID: ${{ secrets.TENCENTCLOUD_SECRET_ID }}
          TENCENTCLOUD_SECRET_KEY: ${{ secrets.TENCENTCLOUD_SECRET_KEY }}
          DUOREADME_BOT_APP_KEY: ${{ secrets.DUOREADME_BOT_APP_KEY }}
```

3. 每次调整 README 或 docs 时，动作将自动将 README 和 docs 翻译成指定的语言。

## 压缩策略

### 1. 文件扫描策略
```
项目根目录
├── README.md （优先读取）
├── .gitignore （用于过滤）
├── src/ （源代码目录）
├── lib/ （库文件目录）
├── docs/ （文档目录）
└── 其他配置文件
```

### 2. 读取优先级
1. **README.md** - 主项目文档，优先读取和压缩处理
2. **源代码文件** - 按重要性读取
3. **配置文件** - 项目配置文件
4. **文档文件** - 其他文档说明

### 3. 内容处理工作流

#### 3.1 文件过滤
- 自动应用 `.gitignore` 规则
- 过滤二进制文件、临时文件、构建产物
- 仅处理文本文件（.md, .py, .js, .java, .cpp 等）

#### 3.2 内容压缩
- **README.md**：压缩至 3000 字符，保留核心内容
- **源代码文件**：智能选择重要文件，每个文件压缩至 2000 字符
- **总内容限制**：每次翻译不超过 15KB，长内容自动分批处理

#### 3.3 智能选择
- 优先选择包含主要逻辑的文件
- 跳过测试文件、示例文件、临时文件
- 保留关键函数定义、类定义、注释

#### 3.4 批量处理机制
当项目内容超过 15KB 时，系统自动分批处理：

```
内容分析 → 文件分组 → 分批翻译 → 结果合并
```

- **文件分组**：按文件类型和重要性分组
- **分批翻译**：每次处理 15KB 的内容
- **结果合并**：智能合并多个批次的结果

### 4. 支持的文件类型
- **文档文件**：.md, .txt, .rst
- **源代码**：.py, .js, .java, .cpp, .c, .go, .rs
- **配置文件**：.yaml, .yml, .json, .toml
- **其他文本**：.sql, .sh, .bat

要求：为每种语言生成完整的翻译，保持原始格式和结构。