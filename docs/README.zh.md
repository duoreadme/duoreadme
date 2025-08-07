<div align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/headerDark.svg" />
    <img src="assets/headerLight.svg" alt="DuoReadme" />
  </picture>

[CI/CD 使用](#github-actions-integration) |
[CLI 使用](#usage) |
[API 使用](#programming-interface) |
[报告问题](https://github.com/duoreadme/duoreadme/issues/new/choose)

</div>

DuoReadme 是一个强大的 CLI 工具，用于自动将项目代码和 README 翻译成多种语言，并生成标准化的多语言文档。

## 功能

- **多语言支持**：支持 100+ 种语言，包括中文、英语、日语、韩语、法语、德语、西班牙语、意大利语、葡萄牙语、俄语等。完整的语言列表，请参见 [ISO 语言代码](./LANGUAGE.md)。
- **智能解析**：自动解析项目结构和代码内容。
  1. 如果项目有 `.gitignore` 文件，它将自动应用过滤规则。
  2. DuoReadme 采用智能项目内容读取策略，确保翻译内容既全面又准确，基于文件和文件夹的级别。
- **批量处理**：一键生成所有语言的 README 文档。
- **腾讯云集成**：与腾讯云智能平台集成。
- **标准配置**：使用常见的项目标准，将英文 README.md 放在根目录中，其他语言的 README.md 文件放在 docs 目录中。
- **GitHub Actions 集成**：使用 GitHub Actions 自动将 README 文件翻译成多种语言。您可以参考 [GitHub Actions 集成](#github-actions-integration) 部分了解更多信息。

## 安装

```bash
pip install duoreadme
```

## 配置

> 您可以查看 [APPLY.md](./APPLY.md) 文件获取更多详细信息。

您可以查看 [config.yaml.example](./config.yaml.example) 文件获取配置文件。

## 使用

### gen - 生成多语言 README（优化高星 README 模板）

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

`trans` 命令是纯文本翻译功能，从项目根目录读取 README 文件并将其翻译成多种语言。与 `gen` 命令不同，`trans` 专注于翻译 README 内容。

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

# 启用调试模式查看详细配置信息
duoreadme config --debug
```

### set - 更新内置配置（仅限开发）
```bash
# 应用新的配置到内置配置（仅限开发/构建）
duoreadme set my_config.yaml
```

### export - 导出内置配置
```bash
# 导出当前内置配置
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

# 创建具有自定义设置的翻译器
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

# 访问翻译内容
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
   1. TENCENTCLOUD_SECRET_ID: 在 [腾讯云控制台](https://console.cloud.tencent.com/cam/capi) 申请，选择 `新建密钥`。
   2. TENCENTCLOUD_SECRET_KEY: 同上。
   3. DUOREADME_BOT_APP_KEY: 在您的 [应用页面](https://lke.cloud.tencent.com/lke#/