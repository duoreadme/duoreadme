> Homepage is English README. You can view the [简体中文](./docs/README.zh.md) | [日本語](./docs/README.ja.md) versions.

# DuoReadme - Multilingual README Generation Tool

DuoReadme is a powerful CLI tool for automatically translating project code and README into multiple languages and generating standardized multilingual documentation.

## Features

- **Multilingual Support**: Supports 100+ languages including Chinese, English, Japanese, Korean, French, German, Spanish, Italian, Portuguese, Russian, etc. For the complete list of languages, please see [ISO Language Codes](./LANGUAGE.md).
- **Smart Parsing**: Automatically parses project structure and code content. 
  1. If the project has a `.gitignore` file, it will automatically apply the filtering rules.
  2. DuoReadme adopts an intelligent project content reading strategy to ensure that the translated content is both comprehensive and accurate, based on the level of the files and folders.
- **Batch Processing**: Generates README documents for all languages with one click.
- **Tencent Cloud Integration**: Integrated with Tencent Cloud Intelligence Platform.
- **Standard Configuration**: Uses common project standards, placing the English README.md in the root directory and other language README.md files in the docs directory.
- **GitHub Actions Integration**: Automatically translate README files to multiple languages using GitHub Actions. You can refer to the [GitHub Actions Integration](#github-actions-integration) section for more details.

## Installation

```bash
pip install duoreadme
```

## Configuration

> You can check the [APPLY.md](./APPLY.md) file for more details.

You can check the [config.yaml.example](./config.yaml.example) file for the configuration file.

## Usage

### gen - Generate Multilingual README (Optimized with high star README template)

```bash
# Generate multilingual README using default settings
duoreadme gen

# Specify languages to translate
duoreadme gen --languages "zh-Hans,en,ja,ko,fr"

# Overall options
Usage: duoreadme gen [OPTIONS]

  Generate multi-language README

Options:
  --project-path TEXT  Project path, defaults to current directory
  --languages TEXT     Languages to generate, comma-separated, e.g.: zh-Hans,en,ja
  --config TEXT        Configuration file path
  --verbose            Show detailed output
  --debug              Enable debug mode, output DEBUG level logs
  --help               Show this message and exit
```

### trans - Only Text Translation

The `trans` command is a pure text translation feature that reads the README file from the project root directory and translates it into multiple languages. Unlike the `gen` command which processes the entire project structure, `trans` focuses solely on translating the README content.

```bash
# Translate README file using default settings
duoreadme trans

# Specify languages to translate
duoreadme trans --languages "zh-Hans,en,ja,ko,fr"

# Overall options
Usage: duoreadme trans [OPTIONS]

  Pure text translation function - translate README file in project root
  directory

Options:
  --project-path TEXT  Project path, defaults to current directory
  --languages TEXT     Languages to translate, comma-separated, e.g.: zh-
                       Hans,en,ja
  --config TEXT        Configuration file path
  --verbose            Show detailed output
  --debug              Enable debug mode, output DEBUG level logs
  --help               Show this message and exit
```

### config - Display Configuration Information
```bash
# Display current built-in configuration
duoreadme config

# Enable debug mode to view detailed configuration information
duoreadme config --debug
```

### set - Update Built-in Configuration (Development Only)
```bash
# Apply a new configuration to the built-in config (for development/build only)
duoreadme set my_config.yaml
```

### export - Export Built-in Configuration
```bash
# Export the current built-in configuration
duoreadme export [-o exported_config.yaml]
```

## Programming Interface

DuoReadme provides a comprehensive Python API for integrating translation functionality into your applications.

```python
from src.core.translator import Translator
from src.core.parser import Parser
from src.utils.config import Config

# Custom configuration
config = Config("custom_config.yaml")

# Create translator with custom settings
translator = Translator(config)

# Translate with specific languages
languages = ["zh-Hans", "en", "ja", "ko"]
result = translator.translate_project(
    project_path="./my_project",
    languages=languages
)

# Parse and process results
parser = Parser()
parsed_content = parser.parse_multilingual_content(result)

# Access translated content
for lang, content in parsed_content.content.items():
    print(f"Language: {lang}")
    print(f"Content: {content[:200]}...")
    print("-" * 50)
```

## GitHub Actions Integration

DuoReadme can be integrated into your GitHub repository using GitHub Actions for automated translation workflows.

### Quick Setup

> You can check the [APPLY.md](./APPLY.md) file for more details.

1. **Configure Secrets**: 
   1. TENCENTCLOUD_SECRET_ID: Apply in [Tencent Cloud Console](https://console.cloud.tencent.com/cam/capi), select `新建密钥`。
   2. TENCENTCLOUD_SECRET_KEY: Same as above.
   3. DUOREADME_BOT_APP_KEY: In your [application page](https://lke.cloud.tencent.com/lke#/app/home), select `调用` then find it in `appkey`.
   4. GH_TOKEN: You can apply GH_TOKEN in `Settings` - `Developer settings` - `Personal access tokens` - `Tokens(classic)` - `Generate new token` - `No expiration` - `Selection: repo and workflow`.
   5. Add required secrets to your repository `your repository` - `settings` - `Securities and variables` - `Actions` - `New repository secret`.

2. **Use the Action**: Add the action file below to your workflow folder `.github/workflows/duoreadme.yml`.

```yaml
# .github/workflows/duoreadme.yml
name: DuoReadme

on:
  push: # You can change the trigger condition.
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
          languages: "zh-Hans,en,ja" # You can specify multiple languages, separated by commas
          translation_mode: "trans" # You can use 'gen' or 'trans' options.
          commit_message: "Update multilingual documentation" # You can customize the commit message.
          debug: "false" # You can enable debug mode to see detailed logs.
        env:
          TENCENTCLOUD_SECRET_ID: ${{ secrets.TENCENTCLOUD_SECRET_ID }}
          TENCENTCLOUD_SECRET_KEY: ${{ secrets.TENCENTCLOUD_SECRET_KEY }}
          DUOREADME_BOT_APP_KEY: ${{ secrets.DUOREADME_BOT_APP_KEY }}
```

3. Every time adjust the README or docs, the action will automatically translate the README and docs to the specified languages.

## Compress Strategy

### 1. File Scanning Strategy
```
Project Root Directory
├── README.md (Priority Read)
├── .gitignore (For Filtering)
├── src/ (Source Code Directory)
├── lib/ (Library Files Directory)
├── docs/ (Documentation Directory)
└── Other Configuration Files
```

### 2. Reading Priority
1. **README.md** - Main project documentation, priority read and compressed processing
2. **Source Code Files** - Read by importance
3. **Configuration Files** - Project configuration files
4. **Documentation Files** - Other documentation explanations

### 3. Content Processing Workflow

#### 3.1 File Filtering
- Automatically apply `.gitignore` rules
- Filter binary files, temporary files, build artifacts
- Only process text files (.md, .py, .js, .java, .cpp, etc.)

#### 3.2 Content Compression
- **README.md**: Compressed to 3000 characters, retaining core content
- **Source Code Files**: Intelligent selection of important files, each file compressed to 2000 characters
- **Total Content Limit**: No more than 15KB per translation, long content automatically processed in batches

#### 3.3 Intelligent Selection
- Prioritize files containing main logic
- Skip test files, sample files, temporary files
- Retain key function definitions, class definitions, comments

### 4. Batch Processing Mechanism
When the project content exceeds 15KB, the system automatically processes in batches:

```
Content Analysis → File Grouping → Batch Translation → Result Merging
```

- **File Grouping**: Group by file type and importance
- **Batch Translation**: Process 15KB of content per batch
- **Result Merging**: Intelligently merge results from multiple batches

### 5. Supported File Types
- **Documentation Files**: `.md`, `.txt`, `.rst`
- **Source Code**: `.py`, `.js`, `.java`, `.cpp`, `.c`, `.go`, `.rs`
- **Configuration Files**: `.yaml`, `.yml`, `.json`, `.toml`
- **Other Text**: `.sql`, `.sh`, `.bat`