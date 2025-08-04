# DuoReadme 快速启动指南

## 🚀 5分钟快速开始

### 1. 安装

```bash
# 克隆项目
git clone https://github.com/your-username/duoreadme.git
cd duoreadme

# 使用安装脚本（推荐）
./scripts/install.sh

# 或手动安装
pip install -r requirements.txt
pip install -e .
```

### 2. 配置

```bash
# 复制配置文件
cp config.yaml.example config.yaml

# 编辑配置文件，填入您的腾讯云凭证
nano config.yaml
```

配置文件示例：
```yaml
# 腾讯云配置
tencent_cloud:
  secret_id: "your_secret_id"
  secret_key: "your_secret_key"
  region: "ap-beijing"
```

### 3. 使用

```bash
# 基本使用（翻译当前目录）
python -m src.cli.main translate

# 指定项目路径
python -m src.cli.main translate --project-path ./myproject

# 指定语言
python -m src.cli.main translate --languages zh,en,ja

# 查看帮助
python -m src.cli.main translate --help
```

**💡 智能文件过滤**

翻译器会自动应用项目的 `.gitignore` 规则，只翻译重要的源代码文件，跳过临时文件、构建产物等。

### 4. 查看结果

翻译完成后，在 `docs` 目录下会生成：
- `README.zh.md` - 中文版本
- `README.en.md` - 英文版本
- `README.ja.md` - 日文版本
- `README_translation_response.txt` - 原始响应

## 📁 项目结构要求

您的项目应该有以下结构：
```
myproject/
├── README.md          # 项目说明
└── src/               # 源代码目录
    ├── main.py
    ├── utils.py
    └── 其他文件...
```

## 🔧 常见问题

### Q: 如何设置腾讯云凭证？
A: 在 `config.yaml` 文件中填入您的 `secret_id` 和 `secret_key`，或设置环境变量：
```bash
export TENCENTCLOUD_SECRET_ID="your_secret_id"
export TENCENTCLOUD_SECRET_KEY="your_secret_key"
```

### Q: 支持哪些语言？
A: 默认支持10种语言：中文、English、日本語、한국어、Français、Deutsch、Español、Italiano、Português、Русский

### Q: 如何自定义输出目录？
A: 使用 `--output-dir` 参数：
```bash
python -m src.cli.main translate --output-dir ./my_docs
```

### Q: 如何不保存原始响应文件？
A: 使用 `--no-save-raw` 参数：
```bash
python -m src.cli.main translate --no-save-raw
```

## 🧪 测试

```bash
# 运行测试
./scripts/run_tests.sh

# 测试示例项目
python -m src.cli.main translate --project-path examples/sample_project
```

## 📚 更多信息

- 📖 [完整文档](README.md)
- 🏗️ [项目结构](PROJECT_STRUCTURE.md)
- 💡 [使用示例](examples/usage_examples.py)

## 🆘 获取帮助

- 查看 [README.md](README.md) 获取详细文档
- 提交 [Issue](https://github.com/your-username/duoreadme/issues)
- 加入 [Discussions](https://github.com/your-username/duoreadme/discussions) 