"""환경 변수(.env)와 봇 전체에서 쓰는 상수."""
import os
from datetime import timedelta
from pathlib import Path

import discord
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")

TOKEN          = os.getenv("DISCORD_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL   = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
# "fast" 면 OpenAI Fast 모드 (더 빠르고 단가 2배). 비우면 일반
OPENAI_SERVICE_TIER = os.getenv("OPENAI_SERVICE_TIER") or None
GUILD_ID       = int(os.getenv("GUILD_ID"))
ROLE_KO        = int(os.getenv("ROLE_KO"))
ROLE_JA        = int(os.getenv("ROLE_JA"))
ROLE_GENSHIN   = int(os.getenv("ROLE_GENSHIN") or 0)
# 처음 실행할 때 번역 + AI 가 켜질 채널. 이후에는 state.json 이 우선한다
DEFAULT_CHANNELS = {
    int(c) for c in os.getenv("TRANSLATE_CHANNEL_IDS", "").split(",") if c.strip()
}

GUILD      = discord.Object(id=GUILD_ID)
STATE_FILE = ROOT / "state.json"

AI_TIMEOUT        = 10                   # 초. 넘기면 Google 번역으로 대체
CONTEXT_SIZE      = 6                    # AI 번역에 문맥으로 넘기는 이전 메시지 수
CONTEXT_MAX_AGE   = timedelta(hours=3)   # 이보다 오래된 메시지는 문맥에서 제외
CONTEXT_MSG_CHARS = 300                  # 문맥에 넣는 메시지 하나의 최대 길이
SPEAKERS_MAX      = 30                   # 채널별로 기억하는 최근 발언자 수
TOPIC_MAX_CHARS   = 100
MATH_MAX_CHARS    = 300
EMBED_MAX_CHARS   = 4096                 # 디스코드 임베드 본문 한도

# 원문 언어별 설정. flag/color 는 번역 답글에 쓰고, role 은 그 언어 사용자 역할
LANG_CONFIG = {
    "ko": {"dest": "ja", "flag": "🇯🇵", "color": 0x5865F2, "role": ROLE_KO},
    "ja": {"dest": "ko", "flag": "🇰🇷", "color": 0xEB459E, "role": ROLE_JA},
}
LANG_NAME = {"ko": "Korean", "ja": "Japanese"}

COLOR_OK       = 0x57F287
COLOR_ERROR    = 0xED4245
COLOR_WARN     = 0xFAA61A
COLOR_INFO     = 0x5865F2
COLOR_AI       = 0x74AA9C
COLOR_FURIGANA = 0xEB459E
