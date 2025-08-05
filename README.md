# DuoReadme - 多语言 README 生成工具

DuoReadme 是一个强大的 CLI 工具，用于将项目代码和 README 自动翻译成多种语言并生成规范化的多语言文档。

## 功能特性

- **多语言支持**: 支持多种主流语言（100+）详细配置项请见[ISO Language Codes](./LANGUAGE.md)。
- **智能解析**: 自动解析项目结构和代码内容
- **批量处理**: 一键生成所有语言的 README 文档
- **腾讯云集成**: 集成腾讯云智能体平台
- **规范配置**: 采用通用项目规范，英文 README.md 放置在文件根目录下，其他语言的 README.md 放置在 docs 目录下。

## 安装

```bash
# 克隆项目
git clone https://github.com/duoreadme/duoreadme.git
cd duoreadme
# 安装依赖
pip install -r requirements.txt
```

## 使用方法

### 基本使用

```bash
# 默认翻译当前目录
python -m src.cli.main

# 指定项目路径
python -m src.cli.main --project-path ./myproject

# 指定要翻译的语言
python -m src.cli.main --languages "zh,en,ja"

# 启用调试模式
python -m src.cli.main --debug

# 显示详细输出
python -m src.cli.main --verbose
```

**📝 关于 .gitignore 支持**

翻译器会自动检测项目根目录下的 `.gitignore` 文件，并过滤掉被忽略的文件和目录。这确保只翻译项目中真正重要的源代码文件，避免处理临时文件、构建产物、依赖包等。

- 如果项目有 `.gitignore` 文件，会自动应用过滤规则
- 如果没有 `.gitignore` 文件，会读取所有文本文件
- 支持标准的 `.gitignore` 语法（通配符、目录模式等）
- 优先读取 `README.md` 文件，然后读取其他源代码文件

**🔍 代码读取整体逻辑**

DuoReadme 采用智能的项目内容读取策略，确保翻译的内容既全面又精准：

### 1. 文件扫描策略
```
项目根目录
├── README.md (优先读取)
├── .gitignore (用于过滤)
├── src/ (源代码目录)
├── lib/ (库文件目录)
├── docs/ (文档目录)
└── 其他配置文件
```

### 2. 读取优先级
1. **README.md** - 项目主要文档，优先读取并压缩处理
2. **源代码文件** - 按重要性排序读取
3. **配置文件** - 项目配置文件
4. **文档文件** - 其他文档说明

### 3. 内容处理流程

#### 3.1 文件过滤
- 自动应用 `.gitignore` 规则
- 过滤二进制文件、临时文件、构建产物
- 只处理文本文件（.md, .py, .js, .java, .cpp 等）

#### 3.2 内容压缩
- **README.md**: 压缩至 3000 字符，保留核心内容
- **源代码文件**: 智能选择重要文件，每个文件压缩至 2000 字符
- **总内容限制**: 单次翻译不超过 15KB，超长内容自动分批处理

#### 3.3 智能选择
- 优先选择包含主要逻辑的文件
- 跳过测试文件、示例文件、临时文件
- 保留关键的函数定义、类定义、注释说明

### 4. 分批处理机制
当项目内容超过 15KB 时，系统会自动分批处理：

```
内容分析 → 文件分组 → 分批翻译 → 结果合并
```

- **文件分组**: 按文件类型和重要性分组
- **分批翻译**: 每批处理 15KB 内容
- **结果合并**: 智能合并多批翻译结果

### 5. 支持的文件类型
- **文档文件**: `.md`, `.txt`, `.rst`
- **源代码**: `.py`, `.js`, `.java`, `.cpp`, `.c`, `.go`, `.rs`
- **配置文件**: `.yaml`, `.yml`, `.json`, `.toml`
- **其他文本**: `.sql`, `.sh`, `.bat`

### 6. 内容优化
- 自动去除重复内容
- 保留关键的结构信息
- 智能压缩长文本，保持可读性
- 优先保留注释和文档字符串



#### config - 显示配置信息
```bash
# 查看当前配置
python -m src.cli.config_cli

# 指定配置文件
python -m src.cli.config_cli --config ./my_config.yaml

# 启用调试模式
python -m src.cli.config_cli --debug
```

### 帮助信息

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

## 配置

### 环境变量

```bash
# 腾讯云配置
export TENCENTCLOUD_SECRET_ID="your_secret_id"
export TENCENTCLOUD_SECRET_KEY="your_secret_key"
# 应用配置
export DUOREADME_BOT_APP_KEY="your_bot_app_key"
```

### 配置文件

复制示例配置文件并填入您的配置：

```bash
cp config.yaml.example config.yaml
nano config.yaml
```

配置文件示例：

```yaml
app:
  bot_app_key: "your_bot_app_key_here"
  visitor_biz_id: "your_visitor_biz_id_here"

tencent_cloud:
  secret_id: "your_secret_id_here"
  secret_key: "your_secret_key_here"
  region: "ap-beijing"
  service: "lke"
  api_version: "2023-11-30"

translation:
  default_languages:
    - "中文"
    - "English"
    - "日本語"
  batch_size: 5
  timeout: 30

sse:
  streaming_throttle: 1
  timeout: 60
```

## 日志

DuoReadme 提供了完整的日志系统，帮助您了解翻译过程的详细情况：

- **DEBUG**: 详细的调试信息（仅在调试模式下显示）
- **INFO**: 一般信息（默认显示）
- **WARNING**: 警告信息
- **ERROR**: 错误信息
- **CRITICAL**: 严重错误信息

### 日志用法

```bash
# 默认只显示 INFO 及以上日志
python -m src.cli.main

# 显示所有级别日志（调试模式）
python -m src.cli.main --debug
```

## 测试

```bash
# 运行所有测试
python -m pytest tests/

# 运行特定测试
python -m pytest tests/test_translator.py
```