"""부가 기능: /tr summary, /tr math, ふりがな."""
import io
import logging

import discord
from discord import app_commands

from .. import ai
from ..config import (
    COLOR_AI, COLOR_ERROR, COLOR_FURIGANA, COLOR_WARN, EMBED_MAX_CHARS, MATH_MAX_CHARS, ROLE_JA, ROLE_KO,
)
from ..furigana import add_furigana
from ..language import has_kanji
from ..mathrender import render_math
from ..ui import notice
from .translation import tr

log = logging.getLogger(__name__)

SUMMARY_MESSAGES = 50
SUMMARY_FORMAT = {
    "ja":   "Output ONLY a Japanese summary in this format — no extra text:\n🇯🇵 (Japanese summary here)",
    "ko":   "Output ONLY a Korean summary in this format — no extra text:\n🇰🇷 (Korean summary here)",
    "both": "Output EXACTLY in this format — no extra text:\n🇰🇷 (Korean summary here)\n🇯🇵 (Japanese summary here)",
}


@tr.command(name="summary", description=f"Summarize the last {SUMMARY_MESSAGES} user messages in this channel")
async def tr_summary(interaction: discord.Interaction):
    await interaction.response.defer()

    messages = [
        msg async for msg in interaction.channel.history(limit=SUMMARY_MESSAGES)
        if not msg.author.bot and msg.content.strip()
    ]
    if not messages:
        await interaction.followup.send(embed=notice("❌ No messages to summarize.", COLOR_ERROR))
        return
    messages.reverse()
    conversation = "\n".join(f"[{msg.author.display_name}]: {msg.content}" for msg in messages)

    # 요청한 사람의 언어 역할로만 요약한다. 역할이 둘 다 있거나 없으면 두 언어 모두
    role_ids = {r.id for r in getattr(interaction.user, "roles", ())}
    has_ko, has_ja = ROLE_KO in role_ids, ROLE_JA in role_ids
    lang = "ja" if has_ja and not has_ko else "ko" if has_ko and not has_ja else "both"

    system = (
        "You are a summarizer for a Korean-Japanese bilingual chat.\n"
        "Read the conversation and write a concise summary.\n"
        "Rules:\n"
        f"1. {SUMMARY_FORMAT[lang]}\n"
        "2. Each summary should be 3-5 sentences.\n"
        "3. Include who said what if important.\n"
        "4. Do NOT translate individual messages — summarize the overall flow."
    )
    tokens_before = ai.usage_stats["prompt"] + ai.usage_stats["completion"]
    try:
        summary = await ai.complete(system, conversation, temperature=0.3, max_tokens=800)
    except Exception:
        log.exception("summary failed")
        await interaction.followup.send(embed=notice("❌ Could not summarize.", COLOR_ERROR))
        return
    tokens_used = ai.usage_stats["prompt"] + ai.usage_stats["completion"] - tokens_before

    embed = discord.Embed(
        title=f"📝 Summary  ·  last {len(messages)} messages",
        description=summary[:EMBED_MAX_CHARS],
        color=COLOR_AI,
    )
    embed.set_footer(text=f"~{tokens_used:,} tokens used")
    await interaction.followup.send(embed=embed)


@tr.command(name="math", description="Render a LaTeX formula as an image")
@app_commands.describe(formula="LaTeX formula, e.g. \\frac{a}{b} + \\sqrt{x}")
async def tr_math(interaction: discord.Interaction, formula: str):
    await interaction.response.defer()
    png = await render_math(formula)
    if png is None:
        await interaction.followup.send(embed=notice(
            f"❌ Could not render this formula.\n```\n{formula[:MATH_MAX_CHARS]}\n```", COLOR_ERROR
        ))
        return
    await interaction.followup.send(file=discord.File(io.BytesIO(png), "math.png"))


# 메시지 우클릭 → 앱 → ふりがな. 결과는 누른 사람에게만 보인다
@app_commands.context_menu(name="ふりがな")
async def furigana_menu(interaction: discord.Interaction, message: discord.Message):
    # 봇의 번역 답글은 본문이 임베드 안에 있다
    text = message.content.strip()
    if not text and message.embeds:
        text = (message.embeds[0].description or "").strip()

    if not has_kanji(text):
        await interaction.response.send_message(
            embed=notice("ℹ️ No kanji in this message.", COLOR_WARN), ephemeral=True
        )
        return

    await interaction.response.defer(ephemeral=True)
    try:
        result = await add_furigana(text)
    except Exception:
        log.exception("furigana failed")
        await interaction.followup.send(embed=notice("❌ Could not add furigana.", COLOR_ERROR), ephemeral=True)
        return
    await interaction.followup.send(embed=notice(result[:EMBED_MAX_CHARS], COLOR_FURIGANA), ephemeral=True)
