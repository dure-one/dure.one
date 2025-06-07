# 두레원? 듀어원?

<a href="./README.md" name="english" class="hide">english</a>

아무려면 어떤가요.<br/>
소기업을위한 프로그램을 만드는 곳입니다.<br/>
오픈소스를 지향합니다.<br/>


## MKDOCS 사용법

이 사이트는 mkdocs를 이용해 만들었습니다. mkdocs는 마크다운 형식으로 웹사이트를 쉽게 만들수 있는 툴로 개발자들 사이에서 많이 사용되고 있습니다. 여러개의 테마 중에서 material 테마를 이용하고 있습니다. 이 테마는 [squidfunk mkdocs insiders](https://squidfunk.github.io/mkdocs-material/insiders/)에서 인사이더 에디션을 구매할 수 있습니다. 인사이더 에디션은 좀더 많은 기능을 사용할 수 있습니다.

이 튜토리얼에서는 인사이더 에디션 구매없이 다중언어로 사이트를 구성하는 방법을 알아 봅니다.

### 1. 사이트 환경 구성 및 프로그램 설치
사이트를 수정하려면 마크다운을 지원하고 파이썬을 지원하는 에디터가 필요합니다. [fleet](https://www.jetbrains.com/ko-kr/fleet/)을 추천합니다. 젯브레인 툴박스를 열어서 fleet를 설치할 수 있습니다.

파이썬을 설치하고 아래 명령어로 venv환경을 구성합니다.
```bash
$ git clone https://github.com/dure-one/dure.one.git
$ cd dure.one
$ python3 -m venv .
```

아래 명령어로 mkdocs 및 필요한 파이썬 패키지를 설치합니다.
```bash
$ pip install -r requirements.txt
```

이제 사이트를 한번 띄워봅니다.
```bash
$ mkdocs serve
```
### 2. 사이트 설정 및 편집
원하는 에디터를 이용해서 mkdocs.yml 파일을 수정하고 저장하면 mkdocs데몬이 자동으로 읽어 들여 사이트에 적용해 볼수 있습니다.

기본정보 설정은 아래와 같습니다. repo_url은 자신이 올릴 사이트의 repository url을 입력합니다.
```
site_name: "dure-one"
site_description: "small applications to help small businesses."
site_url: "https://dure.one/"
repo_url: "https://github.com/dure-one/dure.one"
repo_name: "dure-one/dure.one"
site_dir: "site"
watch: [README.md]
copyright: Copyright &copy; 2025 Dure.one
edit_uri: edit/main/docs/
```

사이트 네비게이션은 아래와 같이 설정할 수 있습니다.

```markdown
# mkdoc.yml 하단부
nav:
  # Korean Tree
  - index.ko.md
  - Programs:
    - programs.ko.md
  - changelog.ko.md
  - credits.ko.md

  # English Tree
  - index.md
  - Programs:
    - programs.md
  - changelog.md
  - credits.md
```
mkdocs가 위의 설정을 읽어서 자동으로 사이트의 메뉴 구성을 해줍니다.

### 3. 사이트 깃허브로 전송

#### A. 깃헙 워크플로우 이용법
문서 편집이 끝나면 깃허브 액션을 이용하거나 mkdocs의 gh-deploy를 이용해서 서버에 전송 할 수 있습니다.

아래는 깃허브 액션입니다. 깃허브에 푸시를 하면 아래 워크플로우가 실행이 됩니다. 스텝별로 소스를 받아서 깃 히스토리에서 changelog를 자동으로 생성하여 CHANGELOG.md 파일에 저장하고 커밋합니다. 그 후에 gh-deploy로 사이트로 배포합니다.

```markdown
<!-- .github/workflows/docs.yml -->
steps:
      - name: Download source
        uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - name: Install Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Git changelog build
        run: git-changelog --provider github > CHANGELOG.md
      - uses: stefanzweifel/git-auto-commit-action@v5
        with:
          commit_message: Add changelog automatically
      - name: Build site
        run: mkdocs build
      - name: Push to github sites
        run: mkdocs gh-deploy --force --clean****
```

#### B. mkdocs gh-deploy 이용법
위의 구성없이 로컬에서 아래 명령어를 수행하면 깃허브의 리파지토리에 gh-deploy 브랜치로 사이트 컴파일 결과를 전송합니다.

```markdown
$ mkdocs gh-deploy
```

이와 같이 하면 mkdocs를 쉽게 이용할 수 있습니다.

### 추가로 읽을거리
* 깃허브 프리는 2000분, 프로는 3000분의 액션 시간을 제공합니다.[[1]](https://docs.github.com/ko/billing/managing-billing-for-your-products/managing-billing-for-github-actions/about-billing-for-github-actions)
* mkdocs-material 인사이더 에디션은 월 $15에 이용할 수 있습니다. [[2]](https://squidfunk.github.io/mkdocs-material/insiders/sponsoring-tiers/#the-individual)
* 깃허브 페이지로 사용자 지정 도메인을 구성 할 수 있습니다.[[3]](https://docs.github.com/ko/pages/configuring-a-custom-domain-for-your-github-pages-site)

