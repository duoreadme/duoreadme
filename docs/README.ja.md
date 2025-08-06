# DuoReadme - 複数言語対応のREADME生成ツール

DuoReadmeは、プロジェクトコードとREADMEを自動的に複数言語に翻訳し、標準化された多言語ドキュメントを生成する強力なCLIツールです。

## 特徴

- **多言語サポート**: 中国語、英語、日本語、韓国語、フランス語、ドイツ語、スペイン語、イタリア語、ポルトガル語、ロシア語など、100以上の言語をサポートしています。完全な言語リストについては、[ISO Language Codes](./LANGUAGE.md)をご覧ください。
- **スマート解析**: プロジェクト構造とコード内容を自動解析します。
- **バッチ処理**: 一括で全ての言語のREADMEドキュメントを生成します。
- **テンセントクラウド統合**: テンセントクラウドインテリジェンスプラットフォームとの統合。
- **標準設定**: 共通のプロジェクト標準を使用し、英語のREADME.mdをルートディレクトリに、他の言語のREADME.mdをdocsディレクトリに配置します。

## インストール

```bash
# プロジェクトをクローン
git clone https://github.com/duoreadme/duoreadme.git
cd duoreadme
# 依存関係をインストール
pip install -r requirements.txt
```

## 使用方法

### 基本的な使用方法

```bash
# 利用可能なすべてのコマンドを表示
python -m src.cli.main --help

# 複数言語のREADMEを生成（.gitignoreによるフィルタリングを自動適用）
python -m src.cli.main gen

# プロジェクトパスを指定して生成
python -m src.cli.main gen --project-path ./myproject

# 翻訳する言語を指定
python -m src.cli.main gen --languages "zh-Hans,en,ja,ko,fr"
```

### 利用可能なコマンド

#### gen - 複数言語のREADMEを生成
```bash
# デフォルト設定を使用して複数言語のREADMEを生成
python -m src.cli.main gen

# プロジェクトパスを指定
python -m src.cli.main gen --project-path ./myproject

# 翻訳する言語を指定
python -m src.cli.main gen --languages "zh-Hans,en,ja,ko,fr"

# 詳細な出力を表示
python -m src.cli.main gen --verbose

# デバッグモードを有効にする（詳細なログを表示）
python -m src.cli.main gen --debug
```

**.gitignoreサポートについて**

翻訳者は、プロジェクトのルートディレクトリにある`.gitignore`ファイルを自動的に検出し、無視されるファイルやディレクトリをフィルタリングします。これにより、プロジェクト内の重要なソースコードファイルのみが翻訳され、一時ファイル、ビルドアーティファクト、依存パッケージなどが処理されることはありません。

- プロジェクトに`.gitignore`ファイルがある場合、自動的にフィルタリングルールが適用されます。
- `.gitignore`ファイルがない場合は、すべてのテキストファイルが読み込まれます。
- 標準の`.gitignore`構文（ワイルドカード、ディレクトリパターンなど）をサポートします。
- `README.md`ファイルを優先的に読み取り、その後他のソースコードファイルを読み取ります。

**🔍 コード全体の読み取りロジック**

DuoReadmeは、翻訳されるコンテンツが包括的かつ正確であることを保証するために、プロジェクト内容のインテリジェントな読み取り戦略を採用しています。

### 1. ファイルスキャン戦略
```
プロジェクトのルートディレクトリ
├── README.md (優先読み取り)
├── .gitignore (フィルタリング用)
├── src/ (ソースコードディレクトリ)
├── lib/ (ライブラリファイルディレクトリ)
├── docs/ (ドキュメントディレクトリ)
└── その他の設定ファイル
```

### 2. 読み取り優先順位
1. **README.md** - メインのプロジェクトドキュメント、優先的に読み取り、圧縮処理を行う
2. **ソースコードファイル** - 重要度に基づいて読み取り
3. **設定ファイル** - プロジェクト設定ファイル
4. **ドキュメントファイル** - その他のドキュメント説明

### 3. コンテンツ処理ワークフロー

#### 3.1 ファイルフィルタリング
- `.gitignore`ルールを自動的に適用
- バイナリファイル、一時ファイル、ビルドアーティファクトをフィルタリング
- テキストファイルのみを処理（.md, .py, .js, .java, .cpp など）

#### 3.2 コンテンツ圧縮
- **README.md**: 3000文字に圧縮し、核心内容を保持
- **ソースコードファイル**: 重要なファイルをインテリジェントに選択し、各ファイルを2000文字に圧縮
- **総コンテンツ制限**: 一度の翻訳で15KBを超えないようにし、長すぎるコンテンツは自動的にバッチ処理

#### 3.3 インテリジェント選択
- 主要ロジックを含むファイルを優先選択
- テストファイル、サンプルファイル、一時ファイルをスキップ
- 重要な関数定義、クラス定義、コメントを保持

### 4. バッチ処理メカニズム
プロジェクト内容が15KBを超えた場合、システムは自動的にバッチ処理を行います:

```
コンテンツ分析 → ファイルグループ分け → バッチ翻訳 → 結果のマージ
```

- **ファイルグループ分け**: ファイルタイプと重要度に基づいてグループ分け
- **バッチ翻訳**: 一度に15KBのコンテンツを処理
- **結果のマージ**: 複数バッチの翻訳結果をインテリジェントにマージ

### 5. サポートされているファイルタイプ
- **ドキュメントファイル**: `.md`, `.txt`, `.rst`
- **ソースコード**: `.py`, `.js`, `.java`, `.cpp`, `.c`, `.go`, `.rs`
- **設定ファイル**: `.yaml`, `.yml`, `.json`, `.toml`
- **その他のテキスト**: `.sql`, `.sh`, `.bat`

### 6. コンテンツ最適化
- 重複するコンテンツを自動的に削除
- 重要な構造情報を保持
- 長いテキストをインテリジェントに圧縮し、読みやすさを維持
- コメントとドキュメント文字列を優先的に保持

#### config - 設定情報の表示
```bash
# 現在の設定を表示
python -m src.cli.main config

# 指定された設定ファイルを表示
python -m src.cli.main config --config ./my_config.yaml

# デバッグモードを有効にして詳細な設定情報を表示
python -m src.cli.main config --debug
```

### グローバルオプション

```bash
# バージョン情報を表示
python -m src.cli.main --version

# ヘルプ情報を表示
python -m src.cli.main --help
```

### プログラミングインターフェース

```python
from src.core.translator import Translator
from src.core.parser import Parser

# 翻訳者を作成
translator = Translator()

# プロジェクト内容を翻訳
result = translator.translate_project("./sample_project")

# 複数言語の内容を解析
parser = Parser()
readme_dict = parser.parse_multilingual_content(result)
```

## 設定

### 環境変数

```bash
# テンセントクラウド設定
export TENCENTCLOUD_SECRET_ID="your_secret_id"
export TENCENTCLOUD_SECRET_KEY="your_secret_key"
# アプリケーション設定
export DUOREADME_BOT_APP_KEY="your_bot_app_key"
```

### 設定ファイル

`config.yaml`ファイルを作成します:

```yaml
# テンセントクラウド設定
tencent_cloud:
  secret_id: "your_secret_id"
  secret_key: "your_secret_key"
  region: "ap-beijing"

# 翻訳設定
translation:
  default_languages:
    # 一般的な言語（推奨）
    - "zh-Hans"    # 中国語（簡体字）
    - "en"         # 英語
    - "ja"         # 日本語
    - "ko"         # 韓国語
    - "fr"         # フランス語
    - "de"         # ドイツ語
    - "es"         # スペイン語
    - "it"         # イタリア語
    - "pt"         # ポルトガル語（ブラジル）
    - "ru"         # ロシア語
    # 完全な言語リストはLANGUAGE.mdを参照してください
  batch_size: 5
  timeout: 30

# ログ設定
logging:
  default_level: "INFO"  # デフォルトのログレベル
  debug_mode: false      # デバッグモードを有効にするかどうか
```

## ログ

DuoReadmeは、翻訳プロセスの詳細を理解するための完全なログシステムを提供します:

### ログレベル

- **DEBUG**: 詳細なデバッグ情報（デバッグモードでのみ表示）
- **INFO**: 一般的な情報（デフォルトで表示）
- **WARNING**: 警告情報
- **ERROR**: エラー情報
- **CRITICAL**: 重大なエラー情報

### 使用方法

#### デフォルトモード
```bash
# INFOレベル以上のログのみを表示
python -m src.cli.main gen
```

#### デバッグモード
```bash
# 全てのログレベルを表示し、詳細なデバッグ情報を含める
python -m src.cli.main gen --debug
```

#### デバッグ情報には以下のものが含まれます
- 設定ファイルのロードプロセス
- ファイルスキャンおよびフィルタリングの詳細
- 翻訳リクエストの詳細情報
- コンテンツ圧縮およびバッチ処理プロセス
- ファイル生成および保存ステップ
- エラーおよび例外の詳細情報

## テスト

```bash
# 全てのテストを実行
python -m pytest tests/

# 特定のテストを実行
python -m pytest tests/test_translator.py
```