"""채널 메시지를 번역해서 답글로 단다."""
import asyncio
import logging
import time

import discord

from . import state
from .config import AI_TIMEOUT, EMBED_MAX_CHARS, LANG_CONFIG
from .language import detect_language, strip_kept
from .memory import build_context, build_participants, remember_message
from .translate import translate_text

log = logging.getLogger(__name__)


async def handle_message(message: discord.Message):
    if message.author.bot or message.channel.id not in state.active_channels:
        return

    content = message.content.strip()
    if not content or content.startswith("!"):   # 다른 봇의 ! 명령어는 건너뛴다
        return

    # 문맥은 현재 메시지를 기록하기 전에 만든다 (자기 자신이 문맥에 들어가지 않도록)
    channel_id = message.channel.id
    context = build_context(channel_id)
    remember_message(message, content)

    lang = detect_language(strip_kept(content))
    if lang is None:
        return
    cfg = LANG_CONFIG[lang]

    # 상대 언어로 쓴 메시지는 번역하지 않는다 (예: 한국어 역할이 일본어로 작성 = 연습 중)
    # 역할이 둘 다 있거나 둘 다 없으면 평소처럼 번역
    role_ids = {r.id for r in getattr(message.author, "roles", ())}
    if LANG_CONFIG[cfg["dest"]]["role"] in role_ids and cfg["role"] not in role_ids:
        return

    try:
        translated = None
        if channel_id in state.ai_channels:
            translated = await _translate_ai(message, content, lang, cfg["dest"], context)
        used_ai = translated is not None
        if translated is None:
            translated = await translate_text(content, lang, cfg["dest"], use_ai=False)

        embed = discord.Embed(title=cfg["flag"], description=translated[:EMBED_MAX_CHARS], color=cfg["color"])
        if used_ai:
            embed.set_footer(text="🤖 AI")
        await message.reply(embed=embed, mention_author=False)
    except Exception:
        log.exception("translation failed in #%s", message.channel)


async def _translate_ai(message: discord.Message, content: str, src: str, dest: str, context: str) -> str | None:
    """AI 번역. 실패하거나 AI_TIMEOUT 을 넘기면 None (호출한 쪽이 Google 번역으로 대체)."""
    channel_id = message.channel.id
    started = time.perf_counter()
    async with message.channel.typing():
        try:
            translated = await asyncio.wait_for(
                translate_text(
                    content, src, dest, use_ai=True, context=context,
                    topic=state.channel_topic.get(channel_id),
                    participants=build_participants(channel_id),
                ),
                timeout=AI_TIMEOUT,
            )
            log.info("AI translation took %.2fs", time.perf_counter() - started)
            return translated
        except asyncio.TimeoutError:
            log.warning("AI translation timed out after %ss, falling back to Google", AI_TIMEOUT)
        except Exception as e:
            log.warning("AI translation failed (%r), falling back to Google", e)
    return None
