<div align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/headerDark.svg" />
    <img src="assets/headerLight.svg" alt="DuoReadme" />
  </picture>

[CI/CD 사용법](#github-actions-integration) | [CLI 사용법](#usage) | [API 사용법](#programming-interface) | [문제 보고](https://github.com/duoreadme/duoreadme/issues/new/choose)

</div>

DuoReadme는 프로젝트 코드와 README를 자동으로 여러 언어로 번역하고 표준화된 다국어 문서를 생성하는 강력한 CLI 도구입니다.

## 주요 기능

- **다국어 지원**: 중국어, 영어, 일본어, 한국어, 프랑스어, 독일어, 스페인어, 이탈리아어, 포르투갈어, 러시아어 등 100개 이상의 언어를 지원합니다. 전체 언어 목록은 [ISO 언어 코드](./LANGUAGE.md)를 참조하세요.
- **지능형 파싱**: 프로젝트 구조와 코드 내용을 자동으로 분석합니다.
  1. 프로젝트에 `.gitignore` 파일이 있는 경우 필터링 규칙을 자동으로 적용합니다.
  2. 파일 및 폴더의 레벨에 기반하여 번역 내용이 포괄적이고 정확하도록 지능형 프로젝트 내용 읽기 전략을 채택합니다.
- **일괄 처리**: 한 번에 모든 언어의 README 문서를 생성합니다.
- **텐센트 클라우드 통합**: 텐센트 클라우드 지능 플랫폼과 통합되었습니다.
- **표준 설정**: 일반적인 프로젝트 표준을 사용하며, 영어 README.md는 루트 디렉토리에 배치하고 다른 언어의 README.md 파일은 docs 디렉토리에 배치합니다.
- **GitHub Actions 통합**: GitHub Actions를 사용하여 README 파일을 자동으로 다국어로 번역합니다. 자세한 내용은 [GitHub Actions 통합](#github-actions-integration) 섹션을 참조하세요.

## 설치

```bash
pip install duoreadme
```

## 설정

> [APPLY.md](./APPLY.md) 파일을 확인하여 자세한 내용을 확인할 수 있습니다.

[config.yaml.example](./config.yaml.example) 파일을 확인하여 설정 파일을 확인할 수 있습니다.

## 사용법

### gen - 다국어 README 생성 (고성능 README 템플릿 최적화)

```bash
# 기본 설정을 사용하여 다국어 README 생성
duoreadme gen

# 번역할 언어 지정
duoreadme gen --languages "zh-Hans,en,ja,ko,fr"

# 전체 옵션
Usage: duoreadme gen [OPTIONS]

  다국어 README 생성

Options:
  --project-path TEXT  프로젝트 경로; 기본값은 현재 디렉토리입니다.
  --languages TEXT     번역할 언어; 쉼표로 구분된 형식으로 예시: zh-Hans,en,ja
  --config TEXT  설정 파일 경로
  --verbose  상세 출력 보기
  --debug  디버그 모드 활성화; DEBUG 레벨 로그 출력
  --help   이 메시지와 함께 종료
```

### trans - 순수 텍스트 번역

`trans` 명령어는 순수 텍스트 번역 기능으로 프로젝트 루트 디렉토리의 README 파일을 다국어로 번역합니다. `gen` 명령어와 달리 `trans`는 전체 프로젝트 구조를 처리하지 않고 단순히 README 내용만 번역합니다.

```bash
# 기본 설정을 사용하여 README 파일 번역
duoreadme trans

# 번역할 언어 지정
duoreadme trans --languages "zh-Hans,en,ja,ko,fr"

# 전체 옵션
Usage: duoreadme trans [OPTIONS]

  순수 텍스트 번역 기능 - 프로젝트 루트 디렉토리의 README 파일 번역

Options:
  --project-path TEXT  프로젝트 경로; 기본값은 현재 디렉토리입니다.
  --languages TEXT     번역할 언어; 쉼표로 구분된 형식으로 예시: zh-Hans,en,ja
  --config TEXT  설정 파일 경로
  --verbose  상세 출력 보기
  --debug  디버그 모드 활성화; DEBUG 레벨 로그 출력
  --help   이 메시지와 함께 종료
```

### config - 설정 정보 표시

```bash
# 내장된 현재 설정 표시
duoreadme config

# 디버그 모드 활성화하여 상세한 설정 정보 보기
duoreadme config --debug
```

### set - 내장된 설정 업데이트 (개발용)

```bash
# 개발/빌드용으로 새 설정을 내장된 설정에 적용합니다.
duoreadme set my_config.yaml
```

### export - 내장된 설정 내보내기

```bash
# 현재 내장된 설정 내보내기
duoreadme export [-o exported_config.yaml]
```

## 프로그래밍 인터페이스

DuoReadme는 애플리케이션에 번역 기능을 통합하기 위해 포괄적인 Python API를 제공합니다.

```python
from src.core.translator import Translator
from src.core.parser import Parser
from src.utils.config import Config

# 커스텀 설정
config = Config("custom_config.yaml")

# 커스텀 설정을 사용하여 번역기 생성하기
translator = Translator(config)

# 특정 언어로 번역하기
languages = ["zh-Hans", "en", "ja", "ko"]
result = translator.translate_project(
    project_path="./my_project",
    languages=languages
)

# 결과 분석 및 처리하기
parser = Parser()
parsed_content = parser.parse_multilingual_content(result)

# 번역 내용 접근하기
for lang, content in parsed_content.content.items():
    print(f"Language: {lang}")
    print(f"Content: {content[:200]}...")
    print("-" * 50)
```

## GitHub Actions 통합

GitHub Actions를 사용하여 DuoReadme를 GitHub 저장소에 통합하면 자동 번역 워크플로우를 구현할 수 있습니다.

### 빠른 설정하기

> [APPLY.md](./APPLY.md) 파일을 확인하여 자세한 내용을 확인할 수 있습니다.

1. **비밀번호 설정**:
   1. TENCENTCLOUD_SECRET_ID: [텐센트 클라우드 콘솔](https://console.cloud.tencent.com/cam/capi)에서 `새로운 비밀번호`를 선택합니다.
   2. TENCENTCLOUD_SECRET_KEY: 동일합니다.
   3. DUOREADME_BOT_APP_KEY: [애플리케이션 페이지](https://lke.cloud.tencent.com/lke#/app/home)에서 `호출`을 선택한 후 `appkey`에서 찾습니다.
   4. GH_TOKEN: `Settings` - `Developer settings` - `Personal access tokens` - `Tokens(classic)` - `Generate new token` - `No expiration` - `Selection: repo and workflow`에서 신청합니다.
   5. 필요한 비밀번호를 저장소 `your repository` - `settings` - `Securities and variables` - `Actions` - `New repository secret`에 추가합니다.

2. **액션 사용하기**: 아래 액션 파일을 워크플로우 폴더 `.github/workflows/duoreadme.yml`에 추가합니다.

```yaml
# .github/workflows/duoreadme.yml
name: DuoReadme

on:
  push: # 트리거 조건을 변경할 수 있습니다.
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

  - name: Custom settings with translation
  uses: duoreadme/duoreadme@v0.1.2
  with:
  languages: "zh-Hans,en,ja" # 쉼표로 구분하여 여러 언어를 지정할 수 있습니다.
  translation_mode: "trans" # 'gen' 또는 'trans' 옵션을 사용할 수 있습니다.
  commit_message: "Update multilingual documentation" # 커밋 메시지를 커스텀할 수 있습니다.
  debug: "false" # 디버그 모드를 활성화하여 상세 로그를 볼 수 있습니다.
  env:
  TENCENTCLOUD_SECRET_ID: ${{ secrets.TENCENTCLOUD_SECRET_ID }}
  TENCENTCLOUD_SECRET_KEY: ${{ secrets.TENCENTCLOUD_SECRET_KEY }}
  DUOREADME_BOT_APP_KEY: ${{ secrets.DUOREADME_BOT_APP_KEY }}
```

3. README 또는 docs를 수정할 때마다 액션은 지정된 언어로 README 및 docs를 자동으로 번역합니다.

## 압축 전략

### 1. 파일 스캔 전략

```
프로젝트 루트 디렉토리
├── README.md (우선 읽기)
├── .gitignore (필터링 위해)
├── src/ (소스 코드 디렉토리)
├── lib/ (라이브러리 파일 디렉토리)
├── docs/ (문档 디렉토리)
└── 기타 설정 파일들...
```

### 2. 읽기 우선순위

1. **README.md** - 주요 프로젝트 문서; 우선 읽기 및 압축 처리합니다.
2. **소스 코드 파일** - 중요성에 따라 읽습니다.
3. **설정 파일** - 프로젝트 설정 파일들입니다.
4. **문档 파일** - 기타 설명 문서입니다.

### 3. 내용 처리 워크플로우

#### 3.1 파일 필터링

- `.gitignore` 규칙 자동 적용하기
- 바이너리 파일, 임시 파일, 빌드 아티팩트 필터링하기
- 텍스트 파일만 처리합니다 (.md, .py, .js, .java, .cpp 등)

#### 3.2 내용 압축하기

- **README.md**: 핵심 내용을 유지하며 압축된 길이를 3000자로 제한합니다.
- **소스 코드 파일**: 중요 파일 선택적으로 처리하며 각 파일을 압축하여 2000자로 제한합니다.
- **전체 내용 한도**: 각 번역당 15KB 이내이며 장황한 내용은 자동으로 일괄 처리됩니다.

#### 3.3 지능형 선택하기

- 주요 논리를 포함하는 파일 우선시하기
- 테스트 파일, 샘플 파일, 임시 파일 건너뛰기
- 핵심 함수 정의, 클래스 정의, 주석 포함시키기

#### 3.4 일괄 처리 메커니즘

프로젝트 내용이 15KB를 초과하면 시스템은 자동으로 일괄 처리합니다:

```
내용 분석 → 파일 그룹화 → 일괄 번역 → 결과 합치기
```

- **파일 그룹화**: 파일 유형과 중요성에 따라 그룹화합니다.
- **일괄 번역**: 한 번에 15KB의 내용 처리합니다.
- **결과 합치기**: 여러 일괄의 결과를 지능적으로 합칩니다.

### 4. 지원하는 파일 유형

- **문档 파일**: `.md`, `.txt`, `.rst`
- **소스 코드**: `.py`, `.js`, `.java`, `.cpp`, `.c`, `.go`, `.rs`
- **설정 파일**: `.yaml`, `.yml`, `.json`, `.toml`
- **기타 텍스트**: `.sql`, `.sh`, `.bat`