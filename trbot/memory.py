"""채널별 대화 기억. AI 번역에 넘기는 <context> 와 <participants>.

메모리에만 있어서 재시작하면 비워진다.
"""
import re
from collections import defaultdict, deque
from datetime import datetime

import discord

from .config import CONTEXT_MAX_AGE, CONTEXT_MSG_CHARS, CONTEXT_SIZE, SPEAKERS_MAX
from .language import is_japanese, is_korean

# 최근 메시지: (작성 시각, 작성자, 원문)
context_history: dict[int, deque[tuple[datetime, str, str]]] = defaultdict(
    lambda: deque(maxlen=CONTEXT_SIZE)
)

# 최근 발언자 닉네임 (오래된 순, 값은 쓰지 않는 순서 있는 집합).
# 문맥에 없는 사람의 이름도 알아보게 한다. 예: 한국인이 "히마"라고 부르면 ひまちゃん 으로 번역
channel_speakers: dict[int, dict[str, None]] = defaultdict(dict)

# 서버 닉네임 형식: "일본어 이름 - 한국어 이름" (예: ひまちゃん - 히마). 순서가 반대여도 된다
NICK_SEP_RE = re.compile(r"\s*-\s*")


def remember_message(message: discord.Message, content: str):
    channel_id = message.channel.id
    name = message.author.display_name
    context_history[channel_id].append((message.created_at, name, content[:CONTEXT_MSG_CHARS]))

    speakers = channel_speakers[channel_id]
    speakers.pop(name, None)   # 다시 넣어서 가장 최근으로 옮긴다
    speakers[name] = None
    if len(speakers) > SPEAKERS_MAX:
        speakers.pop(next(iter(speakers)))


def build_context(channel_id: int) -> str:
    cutoff = discord.utils.utcnow() - CONTEXT_MAX_AGE
    return "\n".join(
        f"[{author}]: {text}"
        for created_at, author, text in context_history[channel_id]
        if created_at >= cutoff
    )


def format_participant(name: str) -> str:
    """'ひまちゃん - 히마' → 'ひまちゃん = 히마'. 형식이 다르면 닉네임 그대로."""
    parts = NICK_SEP_RE.split(name, maxsplit=1)
    if len(parts) == 2:
        ja, ko = parts
        if is_korean(ja) and not is_korean(ko):
            ja, ko = ko, ja
        if is_japanese(ja) and not is_korean(ja) and is_korean(ko):
            return f"{ja} = {ko}"
    return name


def build_participants(channel_id: int) -> str:
    return "\n".join(format_participant(name) for name in channel_speakers[channel_id])
