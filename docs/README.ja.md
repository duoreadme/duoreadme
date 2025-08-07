<div align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/headerDark.svg" />
    <img src="assets/headerLight.svg" alt="DuoReadme" />
  </picture>

[CI/CD の使用方法](#github-actions-integration) |
[CLI の使用方法](#usage) |
[API の使用方法](#programming-interface) |
[問題の報告](https://github.com/duoreadme/duoreadme/issues/new/choose)

</div>

DuoReadmeは、プロジェクトコードとREADMEを自動的に複数言語に翻訳し、標準化された多言語ドキュメントを生成する強力なCLIツールです。

## 特徴

- **多言語対応**：中国語、英語、日本語、韓国語、フランス語、ドイツ語、スペイン語、イタリア語、ポルトガル語、ロシア語など、100以上の言語をサポートしています。完全な言語リストについては、[ISO 言語コード](./LANGUAGE.md)をご覧ください。
- **スマート解析**：プロジェクト構造とコード内容を自動解析します。
  1. プロジェクトに`.gitignore`ファイルがある場合、自動的にフィルタリングルールが適用されます。
  2. DuoReadmeは、ファイルとフォルダーのレベルに基づいて、翻訳内容が包括的かつ正確であることを保証するための、インテリジェントなプロジェクト内容読み取り戦略を採用しています。
- **バッチ処理**：ワンクリックですべての言語のREADMEドキュメントを生成します。
- **テンセントクラウド統合**：テンセントクラウドインテリジェンスプラットフォームとの統合。
- **標準設定**：一般的なプロジェクト標準を使用し、英語のREADME.mdをルートディレクトリに、他の言語のREADME.mdファイルをdocsディレクトリに配置します。
- **GitHub Actions 統合**：GitHub Actionsを使用して、READMEファイルを複数言語に自動翻訳します。詳細については、[GitHub Actions 統合](#github-actions-integration)セクションを参照してください。

## インストール

```bash
pip install duoreadme
```

## 設定

> 詳細については、[APPLY.md](./APPLY.md)ファイルをご覧ください。

設定ファイルについては、[config.yaml.example](./config.yaml.example)ファイルをご覧ください。

## 使用方法

### gen - 複数言語READMEの生成（高評価READMEテンプレートで最適化）

```bash
# デフォルト設定を使用して複数言語READMEを生成
duoreadme gen

# 翻訳する言語を指定
duoreadme gen --languages "zh-Hans,en,ja,ko,fr"

# 全体オプション
Usage: duoreadme gen [OPTIONS]

  複数言語READMEの生成

Options:
  --project-path TEXT  プロジェクトパス、デフォルトは現在のディレクトリ
  --languages TEXT     生成する言語、カンマ区切り、例：zh-Hans,en,ja
  --config TEXT        設定ファイルのパス
  --verbose            詳細な出力を表示
  --debug              デバッグモードを有効にし、DEBUGレベルのログを出力
  --help               このメッセージを表示して終了
```

### trans - テキストのみの翻訳

`trans`コマンドは、プロジェクトのルートディレクトリからREADMEファイルを読み取り、それを複数言語に翻訳する純粋なテキスト翻訳機能です。`gen`コマンドとは異なり、`trans`はREADME内容の翻訳にのみ焦点を当てています。

```bash
# デフォルト設定を使用してREADMEファイルを翻訳
duoreadme trans

# 翻訳する言語を指定
duoreadme trans --languages "zh-Hans,en,ja,ko,fr"

# 全体オプション
Usage: duoreadme trans [OPTIONS]

  プロジェクトのルートディレクトリにあるREADMEファイルの純粋なテキスト翻訳機能

Options:
  --project-path TEXT  プロジェクトパス、デフォルトは現在のディレクトリ
  --languages TEXT     翻訳する言語、カンマ区切り、例：zh-
                       Hans,en,ja
  --config TEXT        設定ファイルのパス
  --verbose            詳細な出力を表示
  --debug              デバッグモードを有効にし、DEBUGレベルのログを出力
  --help               このメッセージを表示して終了
```

### config - 設定情報の表示
```bash
# 現在のビルトイン設定を表示
duoreadme config

# 詳細な設定情報を表示するためにデバッグモードを有効にする
duoreadme config --debug
```

### set - ビルトイン設定の更新（開発専用）
```bash
# ビルトイン設定に新しい設定を適用（開発/ビルド専用）
duoreadme set my_config.yaml
```

### export - ビルトイン設定のエクスポート
```bash
# 現在のビルトイン設定をエクスポート
duoreadme export [-o exported_config.yaml]
```

## プログラミングインターフェース

DuoReadmeは、翻訳機能をアプリケーションに統合するための包括的なPython APIを提供します。

```python
from src.core.translator import Translator
from src.core.parser import Parser
from src.utils.config import Config

# カスタム設定
config = Config("custom_config.yaml")

# カスタム設定で翻訳機を作成
translator = Translator(config)

# 特定の言語で翻訳
languages = ["zh-Hans", "en", "ja", "ko"]
result = translator.translate_project(
    project_path="./my_project",
    languages=languages
)

# 結果の解析と処理
parser = Parser()
parsed_content = parser.parse_multilingual_content(result)

# 翻訳されたコンテンツにアクセス
for lang, content in parsed_content.content.items():
    print(f"Language: {lang}")
    print(f"Content: {content[:200]}...")
    print("-" * 50)
```

## GitHub Actions 統合

DuoReadmeは、自動化された翻訳ワークフローのために、GitHub Actionsを使用してGitHubリポジトリに統合することができます。

### クイックセットアップ

> 詳細については、[APPLY.md](./APPLY.md)ファイルをご覧ください。

1. **シークレットの設定**：
   1. TENCENTCLOUD_SECRET_ID: [テンセントクラウドコンソール](https://console.cloud.tencent.com/cam/capi)で申請し、`新しいキーの作成`を選択します。
   2. TENCENTCLOUD_SECRET_KEY: 上記と同じ。
   3. DUOREADME_BOT_APP_KEY: [アプリケーションページ](https://lke.cloud.tencent.com/lke#/