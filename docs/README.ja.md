# DuoReadme - 複数言語対応のREADME生成ツール

DuoReadmeは、プロジェクトコードとREADMEを複数言語に自動翻訳し、標準化された多言語ドキュメントを生成する強力なCLIツールです。

## 特徴

- **多言語サポート**：中国語、英語、日本語、韓国語、フランス語、ドイツ語、スペイン語、イタリア語、ポルトガル語、ロシア語など、100以上の言語をサポートしています。言語の一覧については、[ISO言語コード](./LANGUAGE.md)をご参照ください。
- **スマート解析**：プロジェクト構造とコード内容を自動的に解析します。
  1. プロジェクトに`.gitignore`ファイルがある場合、自動的にフィルタリングルールが適用されます。
  2. DuoReadmeは、ファイルとフォルダのレベルに基づいて、翻訳内容が包括的かつ正確であることを保証するための、インテリジェントなプロジェクト内容読み取り戦略を採用しています。
- **バッチ処理**：ワンクリックですべての言語のREADMEドキュメントを生成します。
- **Tencent Cloud統合**：Tencent Cloud Intelligence Platformと統合されています。
- **標準設定**：一般的なプロジェクト標準を使用し、英語のREADME.mdをルートディレクトリに、他の言語のREADME.mdファイルをdocsディレクトリに配置します。
- **GitHub Actions統合**：GitHub Actionsを使用してREADMEファイルを複数言語に自動翻訳します。詳細については、[GitHub Actions統合](#github-actions-integration)セクションを参照してください。

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

`trans`コマンドは、プロジェクトのルートディレクトリからREADMEファイルを読み取り、それを複数言語に翻訳する純粋なテキスト翻訳機能です。プロジェクト全体の構造を処理する`gen`コマンドとは異なり、`trans`はREADME内容の翻訳に焦点を当てています。

```bash
# デフォルト設定を使用してREADMEファイルを翻訳
duoreadme trans

# 翻訳する言語を指定
duoreadme trans --languages "zh-Hans,en,ja,ko,fr"

# 全体オプション
Usage: duoreadme trans [OPTIONS]

  プロジェクトのルートディレクトリにあるREADMEファイルを純粋なテキスト翻訳機能で翻訳

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
# 新しい設定をビルトイン設定に適用（開発/ビルド専用）
duoreadme set my_config.yaml
```

### export - ビルトイン設定のエクスポート
```bash
# 現在のビルトイン設定をエクスポート
duoreadme export [-o exported_config.yaml]
```

## プログラミングインターフェース

DuoReadmeは、アプリケーションに翻訳機能を統合するための包括的なPython APIを提供します。

```python
from src.core.translator import Translator
from src.core.parser import Parser
from src.utils.config import Config

# カスタム設定
config = Config("custom_config.yaml")

# カスタム設定を使用して翻訳者を作成
translator = Translator(config)

# 特定の言語で翻訳
languages = ["zh-Hans", "en", "ja", "ko"]
result = translator.translate_project(
    project_path="./my_project",
    languages=languages
)

# 結果を解析および処理
parser = Parser()
parsed_content = parser.parse_multilingual_content(result)

# 翻訳後のコンテンツにアクセス
for lang, content in parsed_content.content.items():
    print(f"Language: {lang}")
    print(f"Content: {content[:200]}...")
    print("-" * 50)
```

## GitHub Actions統合

DuoReadmeは、自動化された翻訳ワークフローのために、GitHub Actionsを使用してGitHubリポジトリに統合することができます。

### クイックセットアップ

> 詳細については、[APPLY.md](./APPLY.md)ファイルをご覧ください。

1. **シークレットの設定**：
   1. TENCENTCLOUD_SECRET_ID: [Tencent Cloudコンソール](https://console.cloud.tencent.com/cam/capi)で申請し、「新しいキー」を選択します。
   2. TENCENTCLOUD_SECRET_KEY: 上記と同じ。
   3. DUOREADME_BOT_APP_KEY: [アプリケーションページ](https://lke.cloud.tencent.com/lke#/)で、「呼び出し」を選択し、「appkey」で見つけることができます。
   4. GH_TOKEN: 「設定」 - 「開発者設定」 - 「パーソナルアクセストークン」 - 「トークン（クラシック）」 - 「新しいトークンの生成」 - 「期限なし」 - 「選択：repoおよびworkflow」でGH_TOKENを申請できます。
   5. 必要なシークレットをリポジトリに追加します。「your repository」 - 「settings」 - 「Securities and variables」 - 「Actions」 - 「New repository secret」。

2. **アクションの使用**：以下のアクションファイルをワークフローフォルダー`.github/workflows/duoreadme.yml`に追加します。

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

      - name: Translate with custom settings
        uses: duoreadme/duoreadme@v0.1.2
        with:
          languages: "zh-Hans,en,ja" # 複数の言語を指定でき、カンマで区切ります
          translation_mode: "trans" # 'gen'または'trans'オプションを使用できます。
          commit_message: "Update multilingual documentation" # コミットメッセージをカスタマイズできます。
          debug: "false" # 詳細なログを表示するためにデバッグモードを有効にできます。
        env:
          TENCENTCLOUD_SECRET_ID: ${{ secrets.TENCENTCLOUD_SECRET_ID }}
          TENCENTCLOUD_SECRET_KEY: ${{ secrets.TENCENTCLOUD_SECRET_KEY }}
          DUOREADME_BOT_APP_KEY: ${{ secrets.DUOREADME_BOT_APP_KEY }}
```

3. READMEやdocsを調整するたびに、アクションが自動的にREADMEとdocsを指定された言語に翻訳します。

## 圧縮戦略

### 1. ファイルスキャン戦略
```
プロジェクトのルートディレクトリ
├── README.md （優先読み取り）
├── .gitignore （フィルタリング用）
├── src/ （ソースコードディレクトリ）
├── lib/ （ライブラリファイルディレクトリ）
├── docs/ （ドキュメントディレクトリ）
└── その他の設定ファイル
```

### 2. 読み取り優先順位
1. **README.md** - メインプロジェクトドキュメント、優先読み取りおよび圧縮処理
2. **ソースコードファイル** - 重要度によって読み取り
3. **設定ファイル** - プロジェクト設定ファイル
4. **ドキュメントファイル** - その他のドキュメント説明

### 3. コンテンツ処理ワークフロー

#### 3.1 ファイルフィルタリング
- `.gitignore`ルールを自動的に適用
- バイナリファイル、一時ファイル、ビルドアーティファクトをフィルタリング
- テキストファイルのみを処理（.md, .py, .js, .java, .cpp など）

#### 3.2 コンテンツ圧縮
- **README.md**：3000文字に圧縮し、核心内容を保持
- **ソースコードファイル**：重要なファイルをインテリジェントに選択し、各ファイルを2000文字に圧縮
- **総コンテンツ制限**：翻訳ごとに最大15KB、長すぎるコンテンツは自動的にバッチ処理

#### 3.3 インテリジェント選択
- 主要ロジックを含むファイルを優先
- テストファイル、サンプルファイル、一時ファイルをスキップ
- キー関数定義、クラス定義、コメントを保持

#### 3.4 バッチ処理メカニズム
プロジェクト内容が15KBを超えた場合、システムは自動的にバッチ処理を行います：

```
コンテンツ分析 → ファイルグループ分け → バッチ翻訳 → 結果のマージ
```

- **ファイルグループ分け**：ファイルタイプと重要度でグループ分け
- **バッチ翻訳**：15KBのコンテンツをバッチごとに処理
- **結果のマージ**：複数バッチからの結果をインテリジェントにマージ

### 4. サポートされるファイルタイプ
- **ドキュメントファイル**：.md, .txt, .rst
- **ソースコード**：.py, .js, .java, .cpp, .c, .go, .rs
- **設定ファイル**：.yaml, .yml, .json, .toml
- **その他のテキスト**：.sql, .sh, .bat

要件：各言語に対して完全な翻訳を生成し、元の形式と構造を維持します。