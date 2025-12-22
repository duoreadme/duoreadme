<div align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/headerDark.svg" />
    <img src="assets/headerLight.svg" alt="DuoReadme" />
  </picture>

[CI/CD 使用方法](#github-actions-integration) | [CLI 使用方法](#usage) | [API 使用方法](#programming-interface) | [問題報告](https://github.com/duoreadme/duoreadme/issues/new/choose)

</div>

DuoReadme は、プロジェクトのコードと README を複数の言語に自動翻訳し、標準化された多言語ドキュメントを生成する強力な CLI ツールです。

## 特徴

- **多言語サポート**: 中国語、英語、日本語、韓国語、フランス語、ドイツ語、スペイン語、イタリア語、ポルトガル語、ロシア語など 100 以上の言語をサポート。言語の完全なリストについては、[ISO 言語コード](./LANGUAGE.md) を参照してください。
- **スマート解析**: プロジェクト構造とコード内容を自動的に解析します。
  1. プロジェクトに `.gitignore` ファイルがある場合、フィルタリングルールを自動的に適用します。
  2. DuoReadme は、ファイルとフォルダのレベルに基づいて、翻訳内容が包括的かつ正確であることを確実にするスマートなプロジェクト内容読み取り戦略を採用しています。
- **バッチ処理**: 一括処理で全言語の README ドキュメントを生成します。
- **Tencent Cloud 統合**: Tencent Cloud Intelligence Platform と統合されています。
- **標準的な設定**: 汎用プロジェクト標準を使用し、英語の README.md をルートディレクトリに配置し、その他の言語の README.md ファイルを docs ディレクトリに配置します。
- **GitHub Actions 統合**: GitHub Actions を使用して README ファイルを多言語に自動翻訳します。詳細については、[GitHub Actions 統合](#github-actions-integration) セクションを参照してください。

## インストール

```bash
pip install duoreadme
```

## 設定

> 詳細については、[APPLY.md](./APPLY.md) ファイルを参照してください。

[config.yaml.example](./config.yaml.example) ファイルを参照して設定ファイルを確認してください。

## 使用方法

### gen - 複数言語 README の生成（高スター README テンプレートで最適化）

```bash
# デフォルト設定を使用して複数言語の README を生成
duoreadme gen

# 翻訳する言語を指定
duoreadme gen --languages "zh-Hans,en,ja"

# 全般オプション
Usage: duoreadme gen [OPTIONS]

  複数言語 README の生成

Options:
  --project-path TEXT  プロジェクトパス、デフォルトは現在のディレクトリ
  --languages TEXT     翻訳する言語、カンマ区切り、例: zh-Hans,en,ja
  --config TEXT  設定ファイルパス
  --verbose  詳細な出力を表示
  --debug  デバッグモードを有効にし、DEBUG レベルのログを出力
  --help   このメッセージを表示して終了
```

### trans - 純粋なテキスト翻訳

`trans` コマンドは、プロジェクトルートディレクトリから README ファイルを読み込み、それを複数の言語に翻訳する純粋なテキスト翻訳機能です。`gen` コマンドとは異なり、`trans` コマンドはプロジェクト全体の構造を処理する代わりに、README コンテンツにのみ焦点を当てて翻訳を行います。

```bash
# デフォルト設定を使用して README ファイルを翻訳
duoreadme trans

# 翻訳する言語を指定
duoreadme trans --languages "zh-Hans,en,ja"

# 全般オプション
Usage: duoreadme trans [OPTIONS]

  純粋なテキスト翻訳機能 - プロジェクトルートディレクトリの README ファイルを翻訳
  Options:
    --project-path TEXT  プロジェクトパス、デフォルトは現在のディレクトリ
    --languages TEXT     翻訳する言語、カンマ区切り、例: zh-Hans,en,ja
    --config TEXT  設定ファイルパス
    --verbose  詳細な出力を表示
    --debug  デバッグモードを有効にし、DEBUG レベルのログを出力
    --help   このメッセージを表示して終了
```

### config - 設定情報を表示

```bash
# 現在の組み込み設定を表示
duoreadme config

# デバッグモードを有効にして詳細な設定情報を表示
duoreadme config --debug
```

### set - 組み込み設定の更新（開発用のみ）

```bash
# 新しい設定を組み込み設定に適用（開発/ビルド用のみ）
duoreadme set my_config.yaml
```

### export - 組み込み設定のエクスポート

```bash
# 現在の組み込み設定をエクスポート
duoreadme export [-o exported_config.yaml]
```

## API 接続

DuoReadme は、翻訳機能をアプリケーションに統合するために、包括的な Python API を提供します。

```python
from src.core.translator import Translator
from src.core.parser import Parser
from src.utils.config import Config

# カスタム設定
config = Config("custom_config.yaml")

# カスタム設定を使用して翻訳器を作成
translator = Translator(config)

# 特定の言語で翻訳
languages = ["zh-Hans", "en", "ja", "ko"]
result = translator.translate_project(
    project_path="./my_project",
    languages=languages
)

# 解析と結果の処理
parser = Parser()
parsed_content = parser.parse_multilingual_content(result)

# 翻訳コンテンツにアクセス
for lang, content in parsed_content.content.items():
    print(f"言語: {lang}")
    print(f"コンテンツ: {content[:200]}...")
    print("-" * 50)
```

## GitHub Actions 統合

DuoReadme を GitHub Actions を使用して自動翻訳ワークフローに統合できます。

### クイックセットアップ

> 詳細については、[APPLY.md](./APPLY.md) ファイルを参照してください。

1. **シークレットの設定**:
   1. TENCENTCLOUD_SECRET_ID: [Tencent Cloud Console](https://console.cloud.tencent.com/cam/capi) で申請し、「新規キー」を選択。
   2. TENCENTCLOUD_SECRET_KEY: 同様に申請します。
   3. DUOREADME_BOT_APP_KEY: [アプリケーションページ](https://lke.cloud.tencent.com/lke#/app/home)で「呼び出し」を選択し、「appkey」で探します。
   4. GH_TOKEN: `Settings` - `Developer settings` - `Personal access tokens` - `Tokens(classic)` - `Generate new token` - `No expiration` - `Selection: repo and workflow` の順に申請します。
   5. 必要なシークレットをリポジトリに追加: `your repository` - `settings` - `Securities and variables` - `Actions` - `New repository secret`.

2. **アクションの使用**: 下記のアクションファイルをワークフォルダの `.github/workflows/duoreadme.yml` に追加します。

```yaml
# .github/workflows/duoreadme.yml
name: DuoReadme

on:
  push: # トリガー条件を変更できます。
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

  - name: カスタム設定を使用した翻訳
  uses: duoreadme/duoreadme@v0.1.2
  with:
  languages: "zh-Hans,en,ja" # 複数の言語をカンマ区切りで指定できます。
  translation_mode: "trans" # 'gen' や 'trans' オプションを使用できます。
  commit_message: "多言語ドキュメントの更新" # コミットメッセージをカスタマイズできます。
  debug: "false" # デバッグモードを有効にして詳細なログを表示できます。
  env:
  TENCENTCLOUD_SECRET_ID: ${{ secrets.TENCENTCLOUD_SECRET_ID }}
  TENCENTCLOUD_SECRET_KEY: ${{ secrets.TENCENTCLOUD_SECRET_KEY }}
  DUOREADME_BOT_APP_KEY: ${{ secrets.DUOREADME_BOT_APP_KEY }}
```

3. README や docs を修正するたびに、アクションが指定された言語に README や docs を自動的に翻訳します。

## 圧縮戦略

### 1. ファイルスキャン戦略

```
プロジェクトルートディレクトリ
├── README.md (優先的な読み込み)
├── .gitignore (フィルタリング用)
├── src/ (ソースコードディレクトリ)
├── lib/ (ライブラリファイルディレクトリ)
├── docs/ (ドキュメントディレクトリ)
└── その他の設定ファイル
```

### 2. 読み込み優先順位

1. **README.md** - 主なプロジェクトドキュメント、優先的に読み込みおよび圧縮処理されます。
2. **ソースコードファイル** - 優先度に基づいて読み込みます。
3. **設定ファイル** - プロジェクト設定ファイル。
4. **ドキュメントファイル** - その他のドキュメント説明。

### 3. コンテンツ処理フロー

#### 3.1 ファイルフィルタリング

- `.gitignore` ルールを自動的に適用します。
- バイナリファイル、一時ファイル、ビルドアーティファクトをフィルタリングします。
- 文字ファイル（`.md`, `.py`, `.js`, `.java`, `.cpp`, 等）のみ処理します。

#### 3.2 コンテンツ圧縮

- **README.md**: コアコンテンツを保持しつつ 3000 文字に圧縮されます。
- **ソースコードファイル**: インテリジェントな重要ファイル選択を行い、各ファイルは 2000 文字に圧縮されます。
- **総コンテンツ制限**: 各翻訳あたり 15KB を超えず、長いコンテンツは自動的にバッチ処理されます。

#### 3.3 インテリジェント選択

- 主なロジックを含むファイルに優先します。
- テストファイル、サンプルファイル、一時ファイルはスキップします。
- キャップションや重要な関数定義、クラス定義は保持します。

#### 3.4 バッチ処理メカニズム

プロジェクトコンテンツが 15KB を超える場合、システムは自動的にバッチ処理を行います：

```
コンテンツ分析 → ファイルグループ化 → バッチ翻訳 → 結果マージング
```

- **ファイルグループ化**: ファイルタイプと重要性に基づいてグループ化します。
- **バッチ翻訳**: 各バッチで 15KB のコンテンツを処理します。
- **結果マージング**: 複数のバッチからの結果をインテリジェントにマージします。

### 4. 対応するファイルタイプ

- **ドキュメントファイル**: `.md`, `.txt`, `.rst`
- **ソースコード**: `.py`, `.js`, `.java`, `.cpp`, `.c`, `.go`, `.rs`
- **設定ファイル**: `.yaml`, `.yml`, `.json`, `.toml`
- **その他のテキスト**: `.sql`, `.sh`, `.bat`