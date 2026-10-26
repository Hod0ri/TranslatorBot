"""임베드와 봇 상태 표시."""
import discord

from . import state
from .config import COLOR_INFO


def notice(text: str, color: int = COLOR_INFO) -> discord.Embed:
    return discord.Embed(description=text, color=color)


async def update_presence(client: discord.Client):
    """번역 중인 채널 수를 봇 상태에 표시한다."""
    active = state.active_channels
    if active:
        ai_count = len(state.ai_channels & active)
        label = f"🤖 AI+Translate ({ai_count} ch)" if ai_count else f"🟢 Translating ({len(active)} ch)"
        status = discord.Status.online
    else:
        label = "🔴 Translation OFF"
        status = discord.Status.idle
    await client.change_presence(
        status=status, activity=discord.Activity(type=discord.ActivityType.watching, name=label)
    )
