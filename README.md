> Homepage is English README. You can view the [简体中文](./docs/README.zh.md) | [日本語](./docs/README.ja.md) versions.

# DuoReadme - Multilingual README Generation Tool

DuoReadme is a powerful CLI tool for automatically translating project code and README into multiple languages and generating standardized multilingual documentation.

## Features

- **Multilingual Support**: Supports 100+ languages including Chinese, English, Japanese, Korean, French, German, Spanish, Italian, Portuguese, Russian, etc. For the complete list of languages, please see [ISO Language Codes](./LANGUAGE.md).
- **Smart Parsing**: Automatically parses project structure and code content.
- **Batch Processing**: Generates README documents for all languages with one click.
- **Tencent Cloud Integration**: Integrated with Tencent Cloud Intelligence Platform.
- **Standard Configuration**: Uses common project standards, placing the English README.md in the root directory and other language README.md files in the docs directory.
- **GitHub Actions Integration**: Automatically translate README files to multiple languages using GitHub Actions. You can refer to the [GitHub Actions Integration](#github-actions-integration) section for more details.

## Installation

```bash
pip install duoreadme
```

## Usage

### Basic Usage

```bash
# View all available commands
duoreadme --help

# Generate multilingual README (automatically applies .gitignore filtering)
duoreadme gen

# Specify project path to generate
duoreadme gen --project-path ./myproject

# Specify languages to translate
duoreadme gen --languages "zh-Hans,en,ja,ko,fr"

# Pure text translation of README file
duoreadme trans --languages "zh-Hans,en,ja"
```

### Available Commands

#### gen - Generate Multilingual README
```bash
# Generate multilingual README using default settings
duoreadme gen

# Specify project path
duoreadme gen --project-path ./myproject

# Specify languages to translate
duoreadme gen --languages "zh-Hans,en,ja,ko,fr"

# Show detailed output
duoreadme gen --verbose

# Enable debug mode (show detailed logs)
duoreadme gen --debug
```

#### trans - Pure Text Translation
```bash
# Translate README file using default settings
duoreadme trans

# Specify project path
duoreadme trans --project-path ./myproject

# Specify languages to translate
duoreadme trans --languages "zh-Hans,en,ja,ko,fr"

# Show detailed output
duoreadme trans --verbose

# Enable debug mode (show detailed logs)
duoreadme trans --debug
```

**About trans Command**

The `trans` command is a pure text translation feature that reads the README file from the project root directory and translates it into multiple languages. Unlike the `gen` command which processes the entire project structure, `trans` focuses solely on translating the README content.

- Reads the README.md file from the project root directory
- Translates the content into specified languages
- Generates multilingual README files using the same parsing and generation logic as `gen`
- Does not include the `code_text` parameter in API requests (pure text translation)
- Supports all the same options as the `gen` command for consistency

**About .gitignore Support**

The translator automatically detects the `.gitignore` file in the project root directory and filters out ignored files and directories. This ensures that only the truly important source code files in the project are translated, avoiding temporary files, build artifacts, dependency packages, etc.

- If the project has a `.gitignore` file, it will automatically apply the filtering rules.
- If there is no `.gitignore` file, it will read all text files.
- Supports standard `.gitignore` syntax (wildcards, directory patterns, etc.).
- Prioritizes reading the `README.md` file, then reads other source code files.

**🔍 Overall Code Reading Logic**

DuoReadme adopts an intelligent project content reading strategy to ensure that the translated content is both comprehensive and accurate:

#### 1. File Scanning Strategy
```
Project Root Directory
├── README.md (Priority Read)
├── .gitignore (For Filtering)
├── src/ (Source Code Directory)
├── lib/ (Library Files Directory)
├── docs/ (Documentation Directory)
└── Other Configuration Files
```

#### 2. Reading Priority
1. **README.md** - Main project documentation, priority read and compressed processing
2. **Source Code Files** - Read by importance
3. **Configuration Files** - Project configuration files
4. **Documentation Files** - Other documentation explanations

#### 3. Content Processing Workflow

##### 3.1 File Filtering
- Automatically apply `.gitignore` rules
- Filter binary files, temporary files, build artifacts
- Only process text files (.md, .py, .js, .java, .cpp, etc.)

##### 3.2 Content Compression
- **README.md**: Compressed to 3000 characters, retaining core content
- **Source Code Files**: Intelligent selection of important files, each file compressed to 2000 characters
- **Total Content Limit**: No more than 15KB per translation, long content automatically processed in batches

##### 3.3 Intelligent Selection
- Prioritize files containing main logic
- Skip test files, sample files, temporary files
- Retain key function definitions, class definitions, comments

#### 4. Batch Processing Mechanism
When the project content exceeds 15KB, the system automatically processes in batches:

```
Content Analysis → File Grouping → Batch Translation → Result Merging
```

- **File Grouping**: Group by file type and importance
- **Batch Translation**: Process 15KB of content per batch
- **Result Merging**: Intelligently merge results from multiple batches

#### 5. Supported File Types
- **Documentation Files**: `.md`, `.txt`, `.rst`
- **Source Code**: `.py`, `.js`, `.java`, `.cpp`, `.c`, `.go`, `.rs`
- **Configuration Files**: `.yaml`, `.yml`, `.json`, `.toml`
- **Other Text**: `.sql`, `.sh`, `.bat`

#### 6. Content Optimization
- Automatically remove duplicate content
- Retain key structural information
- Intelligent compression of long texts, maintaining readability
- Prioritize retention of comments and documentation strings

#### config - Display Configuration Information
```bash
# Display current built-in configuration
duoreadme config

# Enable debug mode to view detailed configuration information
duoreadme config --debug
```

#### set - Update Built-in Configuration (Development Only)
```bash
# Apply a new configuration to the built-in config (for development/build only)
duoreadme set my_config.yaml
```

#### export - Export Built-in Configuration
```bash
# Export the current built-in configuration
duoreadme export -o exported_config.yaml
```

#### Global Options

```bash
# Display version information
duoreadme --version

# Display help information
duoreadme --help
```

#### Programming Interface

```python
from src.core.translator import Translator
from src.core.parser import Parser

# Create translator
translator = Translator()

# Translate project content
result = translator.translate_project("./sample_project")

# Parse multilingual content
parser = Parser()
readme_dict = parser.parse_multilingual_content(result)
```

## Configuration

#### Environment Variables

```bash
# Tencent Cloud Configuration
export TENCENTCLOUD_SECRET_ID="your_secret_id"
export TENCENTCLOUD_SECRET_KEY="your_secret_key"
# Application Configuration
export DUOREADME_BOT_APP_KEY="your_bot_app_key"
```

#### Configuration File (for development/build only)

You can check the [config.yaml.example](./config.yaml.example) file for the configuration file.

## Logs

DuoReadme provides a complete logging system to help you understand the details of the translation process:

#### Log Levels

- **DEBUG**: Detailed debugging information (only displayed in debug mode)
- **INFO**: General information (default display)
- **WARNING**: Warning information
- **ERROR**: Error information
- **CRITICAL**: Serious error information

#### Usage

##### Debug Mode
```bash
# Show all levels of logs, including detailed debugging information
duoreadme gen --debug
```

##### Debug Information Includes
- Configuration file loading process
- File scanning and filtering details
- Detailed information on translation requests
- Content compression and batch processing process
- File generation and saving steps
- Detailed information on errors and exceptions

## GitHub Actions Integration

DuoReadme can be integrated into your GitHub repository using GitHub Actions for automated translation workflows.

### Quick Setup

1. **Configure Secrets**: Add required secrets to your repository:
   ```
   TENCENTCLOUD_SECRET_ID=your_secret_id
   TENCENTCLOUD_SECRET_KEY=your_secret_key
   DUOREADME_BOT_APP_KEY=your_bot_app_key
   ```

2. **Use the Action**: Add the action to your workflow file.

### Basic Usage

#### Simple Translation Workflow
```yaml
# .github/workflows/translate.yml
name: Translate README

on:
  push:
    branches: [ main ]
    paths: [ 'README.md' ]
  workflow_dispatch:

jobs:
  translate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Translate README
        uses: duoreadme/duoreadme@v0.1.0
        env:
          TENCENTCLOUD_SECRET_ID: ${{ secrets.TENCENTCLOUD_SECRET_ID }}
          TENCENTCLOUD_SECRET_KEY: ${{ secrets.TENCENTCLOUD_SECRET_KEY }}
          DUOREADME_BOT_APP_KEY: ${{ secrets.DUOREADME_BOT_APP_KEY }}
```

#### Advanced Usage
```yaml
# .github/workflows/translate.yml
name: Advanced Translation

on:
  push:
    branches: [ main ]
    paths: [ 'README.md', 'docs/**' ]
  workflow_dispatch:

jobs:
  translate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Translate with custom settings
        uses: duoreadme/duoreadme@v0.1.0
        with:
          languages: 'zh-Hans,en,ja' # You can specify multiple languages, separated by commas
          translation_mode: 'trans' # You can use 'gen' or 'trans' options.
          commit_message: 'Update multilingual documentation' # You can customize the commit message.
          debug: 'true' # You can enable debug mode to see detailed logs.
        env:
          TENCENTCLOUD_SECRET_ID: ${{ secrets.TENCENTCLOUD_SECRET_ID }}
          TENCENTCLOUD_SECRET_KEY: ${{ secrets.TENCENTCLOUD_SECRET_KEY }}
          DUOREADME_BOT_APP_KEY: ${{ secrets.DUOREADME_BOT_APP_KEY }}
```

### Manual Trigger

You can manually trigger the action from the GitHub Actions tab:
1. Go to Actions → Translate README → Run workflow
2. Optionally modify the parameters
3. Click "Run workflow"

## Testing

```bash
# Run all tests
python -m pytest tests/

# Run specific test
python -m pytest tests/test_translator.py
```

Requirements: Generate complete translation for each language, maintain original format and structure.