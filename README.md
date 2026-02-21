# KoJa Translator Bot

한국어 ↔ 일본어 자동 번역 Discord 봇
韓国語 ↔ 日本語 自動翻訳 Discord ボット

---

<details open>
<summary>🇰🇷 한국어</summary>

## 소개

Discord 채널에서 한국어와 일본어를 자동으로 번역해주는 봇입니다.
Google 번역과 OpenAI(GPT) 번역 두 가지 모드를 지원하며, 역할 기반 대화 요약 기능을 제공합니다.

## 요구사항

- Python 3.11+
- Discord 봇 토큰
- OpenAI API 키 (AI 번역 / 요약 사용 시)

## 설치

```bash
# 가상환경 생성 및 활성화
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux

# 패키지 설치
pip install -r requirements.txt
```

## 환경변수 설정

`.env.example`을 복사하여 `.env`로 만들고 값을 입력합니다.

```bash
cp .env.example .env
```

| 변수 | 설명 | 필수 |
|------|------|------|
| `DISCORD_TOKEN` | Discord 봇 토큰 | ✅ |
| `OPENAI_API_KEY` | OpenAI API 키 | ✅ |
| `GUILD_ID` | Discord 서버 ID | ✅ |
| `ROLE_KO` | 한국인 역할 ID | ✅ |
| `ROLE_JA` | 일본인 역할 ID | ✅ |
| `TRANSLATE_CHANNEL_IDS` | 기본 번역 채널 ID (쉼표 구분) | ✖ |
| `OPENAI_MODEL` | OpenAI 모델 (기본: `gpt-4o-mini`) | ✖ |

### ID 확인 방법

Discord 설정 → 고급 → **개발자 모드** 활성화 후
- 서버 아이콘 우클릭 → **서버 ID 복사**
- 채널 우클릭 → **채널 ID 복사**
- 역할 우클릭 → **역할 ID 복사**

## Discord Developer Portal 설정

1. [discord.com/developers/applications](https://discord.com/developers/applications) 접속
2. **Bot** 탭 → `MESSAGE CONTENT INTENT` **ON**
3. **OAuth2** → URL Generator → Scopes: `bot`, `applications.commands`
   Permissions: `Send Messages`, `Read Messages`, `Read Message History`
4. 생성된 URL로 서버에 봇 초대

## 실행

```bash
python bot.py
```

## 슬래시 커맨드

| 커맨드 | 설명 |
|--------|------|
| `/tr on` | 현재 채널 번역 켜기 |
| `/tr off` | 현재 채널 번역 끄기 |
| `/tr status` | 현재 채널 상태 확인 |
| `/tr credits` | OpenAI 사용량 및 예상 비용 조회 |
| `/tr summary` | 최근 메시지 요약 (역할에 따라 언어 자동 선택) |
| `/tr ai on` | AI 번역 켜기 (번역이 ON인 채널만 가능) |
| `/tr ai off` | AI 번역 끄기 → Google 번역으로 전환 |

## 대화 요약 동작 방식

`/tr summary` 실행 시 최근 50개 메시지(봇 제외)를 읽어 요약합니다.
명령어를 실행한 사용자의 역할에 따라 출력 언어가 자동 결정됩니다.

| 역할 | 요약 출력 |
|------|----------|
| 한국인 역할 | 🇰🇷 한국어 요약만 |
| 일본인 역할 | 🇯🇵 일본어 요약만 |
| 둘 다 / 없음 | 🇰🇷 + 🇯🇵 양쪽 모두 |

## 번역 동작 방식

```
사용자 메시지
    ↓
언어 감지 (한국어 / 일본어)
    ↓
번역 (Google Translate 또는 OpenAI GPT)
    ↓
embed로 reply
```

- **Google 번역**: 빠름, 무료, 반복 메시지 캐싱
- **AI 번역**: 자연스러운 번역, 뉘앙스 보존, 유료 (gpt-4o-mini 기준 매우 저렴)

</details>

---

<details open>
<summary>🇯🇵 日本語</summary>

## 概要

Discordチャンネルで韓国語と日本語を自動翻訳するBotです。
Google翻訳とOpenAI（GPT）翻訳の2つのモードに対応し、ロールベースの会話要約機能も搭載しています。

## 動作環境

- Python 3.11+
- Discordボットトークン
- OpenAI APIキー（AI翻訳・要約使用時）

## インストール

```bash
# 仮想環境の作成・有効化
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux

# パッケージのインストール
pip install -r requirements.txt
```

## 環境変数の設定

`.env.example`をコピーして`.env`を作成し、値を入力します。

```bash
cp .env.example .env
```

| 変数 | 説明 | 必須 |
|------|------|------|
| `DISCORD_TOKEN` | Discordボットトークン | ✅ |
| `OPENAI_API_KEY` | OpenAI APIキー | ✅ |
| `GUILD_ID` | DiscordサーバーID | ✅ |
| `ROLE_KO` | 韓国人ロールID | ✅ |
| `ROLE_JA` | 日本人ロールID | ✅ |
| `TRANSLATE_CHANNEL_IDS` | デフォルト翻訳チャンネルID（カンマ区切り） | ✖ |
| `OPENAI_MODEL` | OpenAIモデル（デフォルト: `gpt-4o-mini`） | ✖ |

### IDの確認方法

Discordの設定 → 詳細設定 → **開発者モード**をONにして
- サーバーアイコンを右クリック → **サーバーIDをコピー**
- チャンネルを右クリック → **チャンネルIDをコピー**
- ロールを右クリック → **ロールIDをコピー**

## Discord Developer Portalの設定

1. [discord.com/developers/applications](https://discord.com/developers/applications) にアクセス
2. **Bot** タブ → `MESSAGE CONTENT INTENT` を **ON**
3. **OAuth2** → URL Generator → Scopes: `bot`, `applications.commands`
   Permissions: `Send Messages`, `Read Messages`, `Read Message History`
4. 生成されたURLでサーバーにBotを招待

## 起動

```bash
python bot.py
```

## スラッシュコマンド

| コマンド | 説明 |
|----------|------|
| `/tr on` | このチャンネルの翻訳をON |
| `/tr off` | このチャンネルの翻訳をOFF |
| `/tr status` | このチャンネルの状態を確認 |
| `/tr credits` | OpenAI使用量・推定コストを確認 |
| `/tr summary` | 最近のメッセージを要約（ロールに応じて言語自動選択） |
| `/tr ai on` | AI翻訳をON（翻訳がONのチャンネルのみ） |
| `/tr ai off` | AI翻訳をOFF → Google翻訳に切り替え |

## 会話要約の動作

`/tr summary`を実行すると、最新50件のメッセージ（Bot除く）を読み込んで要約します。
コマンドを実行したユーザーのロールに応じて、出力言語が自動的に決まります。

| ロール | 要約の出力 |
|--------|-----------|
| 韓国人ロール | 🇰🇷 韓国語のみ |
| 日本人ロール | 🇯🇵 日本語のみ |
| 両方 / なし | 🇰🇷 + 🇯🇵 両方 |

## 翻訳の動作

```
ユーザーのメッセージ
    ↓
言語検出（韓国語 / 日本語）
    ↓
翻訳（Google翻訳 または OpenAI GPT）
    ↓
embedでreply
```

- **Google翻訳**: 高速、無料、繰り返しメッセージはキャッシュ
- **AI翻訳**: 自然な翻訳、ニュアンス保持、有料（gpt-4o-mini基準で非常に安価）

</details>
