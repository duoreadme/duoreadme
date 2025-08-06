> これは英語のREADMEです。他の言語バージョンについては、[docs](./docs) ディレクトリをご覧ください。

# DuoReadme - 複数言語対応のREADME生成ツール

DuoReadmeは、プロジェクトコードとREADMEを複数言語に自動翻訳し、標準化された多言語ドキュメントを生成する強力なCLIツールです。

## 特徴

- **多言語サポート**：中国語、英語、日本語、韓国語、フランス語、ドイツ語、スペイン語、イタリア語、ポルトガル語、ロシア語など、100以上の言語をサポートしています。完全な言語リストについては、[ISO言語コード](./LANGUAGE.md)をご覧ください。
- **スマート解析**：プロジェクト構造とコード内容を自動的に解析します。
- **バッチ処理**：ワンクリックですべての言語のREADMEドキュメントを生成します。
- **テンセントクラウド統合**：テンセントクラウドインテリジェンスプラットフォームと統合されています。
- **標準設定**：一般的なプロジェクト標準を使用し、英語のREADME.mdをルートディレクトリに、その他の言語のREADME.mdファイルをdocsディレクトリに配置します。

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

# 複数言語のREADMEを生成（.gitignoreフィルタリングを自動適用）
python -m src.cli.main gen

# 生成するプロジェクトパスを指定
python -m src.cli.main gen --project-path ./myproject

# 翻訳する言語を指定
python -m src.cli.main gen --languages "zh-Hans,en,ja,ko,fr"

# READMEファイルの純粋なテキスト翻訳
python -m src.cli.main trans --languages "zh-Hans,en,ja"
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

#### trans - 純粋なテキスト翻訳
```bash
# デフォルト設定を使用してREADMEファイルを翻訳
python -m src.cli.main trans

# プロジェクトパスを指定
python -m src.cli.main trans --project-path ./myproject

# 翻訳する言語を指定
python -m src.cli.main trans --languages "zh-Hans,en,ja,ko,fr"

# 詳細な出力を表示
python -m src.cli.main trans --verbose

# デバッグモードを有効にする（詳細なログを表示）
python -m src.cli.main trans --debug
```

**transコマンドについて**

`trans`コマンドは、プロジェクトのルートディレクトリからREADMEファイルを読み取り、それを複数言語に翻訳する純粋なテキスト翻訳機能です。プロジェクト全体の構造を処理する`gen`コマンドとは異なり、`trans`はREADMEの内容にのみ焦点を当てています。

- プロジェクトのルートディレクトリからREADME.mdファイルを読み取る
- 指定された言語に内容を翻訳する
- `gen`と同じ解析および生成ロジックを使用して、複数言語のREADMEファイルを生成する
- APIリクエストに`code_text`パラメータを含めない（純粋なテキスト翻訳）
- `gen`コマンドと同じすべてのオプションをサポートして一貫性を保つ

**.gitignoreサポートについて**

翻訳者は、プロジェクトのルートディレクトリにある`.gitignore`ファイルを自動的に検出し、無視されるファイルやディレクトリをフィルタリングします。これにより、プロジェクト内の本当に重要なソースコードファイルのみが翻訳され、一時ファイル、ビルドアーティファクト、依存パッケージなどが回避されます。

- プロジェクトに`.gitignore`ファイルがある場合、自動的にフィルタリングルールが適用される。
- `.gitignore`ファイルがない場合、すべてのテキストファイルが読み取られる。
- 標準の`.gitignore`構文（ワイルドカード、ディレクトリパターンなど）をサポート。
- `README.md`ファイルを優先的に読み取り、その後他のソースコードファイルを読み取る。

**🔍 全体的なコードリーディングロジック**

DuoReadmeは、翻訳される内容が包括的かつ正確であることを確保するために、プロジェクト内容のインテリジェントなリーディング戦略を採用しています：

#### 1. ファイルスキャン戦略
```
プロジェクトのルートディレクトリ
├── README.md （優先読取）
├── .gitignore （フィルタリング用）
├── src/ （ソースコードディレクトリ）
├── lib/ （ライブラリファイルディレクトリ）
├── docs/ （ドキュメントディレクトリ）
└── その他の設定ファイル
```

#### 2. 読み取り優先順位
1. **README.md** - メインプロジェクトドキュメント、優先的に読み取りおよび圧縮処理
2. **ソースコードファイル** - 重要度に基づいて読み取り
3. **設定ファイル** - プロジェクト設定ファイル
4. **ドキュメントファイル** - その他のドキュメント説明

#### 3. コンテンツ処理ワークフロー

##### 3.1 ファイルフィルタリング
- `.gitignore`ルールを自動的に適用
- バイナリファイル、一時ファイル、ビルドアーティファクトをフィルタリング
- テキストファイルのみを処理（.md, .py, .js, .java, .cppなど）

##### 3.2 コンテンツ圧縮
- **README.md**：3000文字に圧縮し、核心内容を保持
- **ソースコードファイル**：重要なファイルをインテリジェントに選択し、各ファイルを2000文字に圧縮
- **総コンテンツ制限**：翻訳ごとに最大15KB、長すぎるコンテンツは自動的にバッチ処理

##### 3.3 インテリジェント選択
- 主要ロジックを含むファイルを優先的に選択
- テストファイル、サンプルファイル、一時ファイルをスキップ
- キーとなる関数定義、クラス定義、コメントを保持

#### 4. バッチ処理メカニズム
プロジェクト内容が15KBを超える場合、システムは自動的にバッチ処理を行います：

```
コンテンツ分析 → ファイルグループ分け → バッチ翻訳 → 結果のマージ
```

- **ファイルグループ分け**：ファイルタイプと重要度に基づいてグループ分け
- **バッチ翻訳**：1回のバッチで15KBのコンテンツを処理
- **結果のマージ**：複数バッチからの結果をインテリジェントにマージ

#### 5. サポートされているファイルタイプ
- **ドキュメントファイル**：.md, .txt, .rst
- **ソースコード**：.py, .js, .java, .cpp, .c, .go, .rs
- **設定ファイル**：.yaml, .yml, .json, .toml
- **その他のテキスト**：.sql, .sh, .bat

#### 6. コンテンツ最適化
- 重複するコンテンツを自動的に削除
- キーとなる構造情報を保持
- 長いテキストをインテリジェントに圧縮し、読みやすさを維持
- コメントとドキュメント文字列の保持を優先

#### config - 設定情報の表示
```bash
# 現在の設定を表示
python -m src.cli.main config

# 指定された設定ファイルを表示
python -m src.cli.main config --config ./my_config.yaml

# デバッグモードを有効にして詳細な設定情報を表示
python -m src.cli.main config --debug
```

#### グローバルオプション

```bash
# バージョン情報を表示
python -m src.cli.main --version

# ヘルプ情報を表示
python -m src.cli.main --help
```

#### プログラミングインターフェース

```python
from src.core.translator import Translator
from src.core.parser import Parser

# 翻訳器を作成
translator = Translator()

# プロジェクト内容を翻訳
result = translator.translate_project("./sample_project")

# 複数言語の内容を解析
parser = Parser()
readme_dict = parser.parse_multilingual_content(result)
```

## 設定

#### 環境変数

```bash
# テンセントクラウド設定
export TENCENTCLOUD_SECRET_ID="your_secret_id"
export TENCENTCLOUD_SECRET_KEY="your_secret_key"
# アプリケーション設定
export DUOREADME_BOT_APP_KEY="your_bot_app_key"
```

#### 設定ファイル

`config.yaml`ファイルを作成：

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
    # 言語の完全なリストについては、LANGUAGE.mdを参照してください
  batch_size: 5
  timeout: 30

# ロギング設定
logging:
  default_level: "INFO"  # デフォルトのログレベル
  debug_mode: false      # デバッグモードを有効にするかどうか
```

## ログ

DuoReadmeは、翻訳プロセスの詳細を理解するのに役立つ完全なログシステムを提供します：

#### ログレベル

- **DEBUG**：詳細なデバッグ情報（デバッグモードでのみ表示）
- **INFO**：一般的な情報（デフォルトで表示）
- **WARNING**：警告情報
- **ERROR**：エラー情報
- **CRITICAL**：重大なエラー情報

#### 使用方法

##### デフォルトモード
```bash
# INFOレベル以上のログのみを表示
python -m src.cli.main gen
```

##### デバッグモード
```bash
# 詳細なデバッグ情報を含むすべてのレベルのログを表示
python -m src.cli.main gen --debug
```

##### デバッグ情報には以下のものが含まれます
- 設定ファイルのロードプロセス
- ファイルスキャンとフィルタリングの詳細
- 翻訳リクエストの詳細情報
- コンテンツ圧縮とバッチ処理プロセス
- ファイル生成と保存ステップ
- エラーと例外の詳細情報

## テスト

```bash
# すべてのテストを実行
python -m pytest tests/

# 特定のテストを実行
python -m pytest tests/test_translator.py
```

要件：各言語に対して完全な翻訳を生成し、元の形式と構造を保持します。