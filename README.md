> This is the English README. For other language versions, please see the [docs](./docs) directory.

# DuoReadme - Multilingual README Generation Tool

DuoReadme is a powerful CLI tool for automatically translating project code and README into multiple languages and generating standardized multilingual documentation.

## Features

- **Multilingual Support**: Supports 100+ languages including Chinese, English, Japanese, Korean, French, German, Spanish, Italian, Portuguese, Russian, etc. For the complete list of languages, please see [ISO Language Codes](./LANGUAGE.md).
- **Smart Parsing**: Automatically parses project structure and code content.
- **Batch Processing**: Generates README documents for all languages with one click.
- **Tencent Cloud Integration**: Integrated with Tencent Cloud Intelligence Platform.
- **Standard Configuration**: Uses common project standards, placing the English README.md in the root directory and other language README.md files in the docs directory.

## Installation

```bash
# Clone the project
git clone https://github.com/duoreadme/duoreadme.git
cd duoreadme
# Install dependencies
pip install -r requirements.txt
```

## Usage

### Basic Usage

```bash
# View all available commands
python -m src.cli.main --help

# Generate multilingual README (automatically applies .gitignore filtering)
python -m src.cli.main gen

# Specify project path to generate
python -m src.cli.main gen --project-path ./myproject

# Specify languages to translate
python -m src.cli.main gen --languages "zh-Hans,en,ja,ko,fr"

# Pure text translation of README file
python -m src.cli.main trans --languages "zh-Hans,en,ja"
```

### Available Commands

#### gen - Generate Multilingual README
```bash
# Generate multilingual README using default settings
python -m src.cli.main gen

# Specify project path
python -m src.cli.main gen --project-path ./myproject

# Specify languages to translate
python -m src.cli.main gen --languages "zh-Hans,en,ja,ko,fr"

# Show detailed output
python -m src.cli.main gen --verbose

# Enable debug mode (show detailed logs)
python -m src.cli.main gen --debug
```

#### trans - Pure Text Translation
```bash
# Translate README file using default settings
python -m src.cli.main trans

# Specify project path
python -m src.cli.main trans --project-path ./myproject

# Specify languages to translate
python -m src.cli.main trans --languages "zh-Hans,en,ja,ko,fr"

# Show detailed output
python -m src.cli.main trans --verbose

# Enable debug mode (show detailed logs)
python -m src.cli.main trans --debug
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

### 6. Content Optimization
- Automatically remove duplicate content
- Retain key structural information
- Intelligent compression of long texts, maintaining readability
- Prioritize retention of comments and documentation strings

#### config - Display Configuration Information
```bash
# Display current configuration
python -m src.cli.main config

# Display specified configuration file
python -m src.cli.main config --config ./my_config.yaml

# Enable debug mode to view detailed configuration information
python -m src.cli.main config --debug
```

### Global Options

```bash
# Display version information
python -m src.cli.main --version

# Display help information
python -m src.cli.main --help
```

### Programming Interface

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

### Environment Variables

```bash
# Tencent Cloud Configuration
export TENCENTCLOUD_SECRET_ID="your_secret_id"
export TENCENTCLOUD_SECRET_KEY="your_secret_key"
# Application Configuration
export DUOREADME_BOT_APP_KEY="your_bot_app_key"
```

### Configuration File

Create `config.yaml` file:

```yaml
# Tencent Cloud Configuration
tencent_cloud:
  secret_id: "your_secret_id"
  secret_key: "your_secret_key"
  region: "ap-beijing"

# Translation Configuration
translation:
  default_languages:
    # Common languages (recommended)
    - "zh-Hans"    # Chinese (Simplified)
    - "en"         # English
    - "ja"         # Japanese
    - "ko"         # Korean
    - "fr"         # French
    - "de"         # German
    - "es"         # Spanish
    - "it"         # Italian
    - "pt"         # Portuguese (Brazil)
    - "ru"         # Russian
    # Complete list of languages refer to LANGUAGE.md
  batch_size: 5
  timeout: 30

# Logging Configuration
logging:
  default_level: "INFO"  # Default log level
  debug_mode: false      # Whether to enable debug mode
```

## Logs

DuoReadme provides a complete logging system to help you understand the details of the translation process:

### Log Levels

- **DEBUG**: Detailed debugging information (only displayed in debug mode)
- **INFO**: General information (default display)
- **WARNING**: Warning information
- **ERROR**: Error information
- **CRITICAL**: Serious error information

### Usage

#### Default Mode
```bash
# Only show logs at INFO level and above
python -m src.cli.main gen
```

#### Debug Mode
```bash
# Show all levels of logs, including detailed debugging information
python -m src.cli.main gen --debug
```

#### Debug Information Includes
- Configuration file loading process
- File scanning and filtering details
- Detailed information on translation requests
- Content compression and batch processing process
- File generation and saving steps
- Detailed information on errors and exceptions

## Testing

```bash
# Run all tests
python -m pytest tests/

# Run specific test
python -m pytest tests/test_translator.py
```