"""/tr 번역 설정 커맨드."""
import discord
from discord import app_commands

from .. import ai, state
from ..config import COLOR_AI, COLOR_ERROR, COLOR_INFO, COLOR_OK, COLOR_WARN, OPENAI_MODEL, TOPIC_MAX_CHARS
from ..ui import notice, update_presence

tr    = app_commands.Group(name="tr", description="Translation bot commands")
tr_ai = app_commands.Group(name="ai", description="AI translation commands", parent=tr)


@tr.command(name="on", description="Enable translation (AI) in this channel")
async def tr_on(interaction: discord.Interaction):
    state.active_channels.add(interaction.channel_id)
    state.ai_channels.add(interaction.channel_id)
    state.save()
    await update_presence(interaction.client)
    await interaction.response.send_message(
        embed=notice("✅ Translation **enabled** in this channel. (🤖 AI)", COLOR_OK)
    )


@tr.command(name="off", description="Disable translation in this channel")
async def tr_off(interaction: discord.Interaction):
    state.active_channels.discard(interaction.channel_id)
    state.ai_channels.discard(interaction.channel_id)
    state.save()
    await update_presence(interaction.client)
    await interaction.response.send_message(
        embed=notice("⛔ Translation **disabled** in this channel.", COLOR_ERROR)
    )


@tr.command(name="status", description="Check translation status in this channel")
async def tr_status(interaction: discord.Interaction):
    ch = interaction.channel_id
    topic = state.channel_topic.get(ch)
    embed = discord.Embed(title="📊 Translation Status", color=COLOR_INFO)
    embed.add_field(name="Translation", value="**ON** ✅" if ch in state.active_channels else "**OFF** ⛔")
    embed.add_field(name="AI Mode", value="**ON** 🤖" if ch in state.ai_channels else "**OFF** (Google)")
    embed.add_field(name="Topic", value=f"🎮 **{topic}**" if topic else "—")
    await interaction.response.send_message(embed=embed)


@tr.command(name="topic", description="Set the chat topic (e.g. a game) so AI uses its official names")
@app_commands.describe(topic="e.g. 원신 / Genshin Impact (leave empty to clear)")
async def tr_topic(interaction: discord.Interaction, topic: str | None = None):
    ch = interaction.channel_id
    if topic is None:
        state.channel_topic.pop(ch, None)
        state.save()
        await interaction.response.send_message(embed=notice("🎮 Topic **cleared** in this channel."))
        return

    # 시스템 프롬프트에 들어가므로 한 줄로 짧게 자른다
    topic = " ".join(topic.split())[:TOPIC_MAX_CHARS]
    state.channel_topic[ch] = topic
    state.save()
    embed = notice(f"🎮 Topic set to **{topic}**.", COLOR_OK)
    if ch not in state.ai_channels:
        embed.set_footer(text="⚠️ Topic only applies to AI translation. Turn it on with /tr ai on")
    await interaction.response.send_message(embed=embed)


@tr.command(name="credits", description="Show OpenAI usage and estimated cost since the bot started")
async def tr_credits(interaction: discord.Interaction):
    usage = ai.usage_stats
    cost = ai.estimated_cost()
    embed = discord.Embed(title="📊 OpenAI Usage (this session)", color=COLOR_AI)
    embed.add_field(name="API Calls",     value=f"{usage['calls']:,}")
    embed.add_field(name="Input tokens",  value=f"{usage['prompt']:,}")
    embed.add_field(name="Output tokens", value=f"{usage['completion']:,}")
    embed.add_field(
        name="Estimated cost",
        value=f"**${cost:.4f}**" if cost is not None else "unknown (add this model to ai.PRICES)",
        inline=False,
    )
    embed.set_footer(text=f"{OPENAI_MODEL} · resets on bot restart · full history: platform.openai.com/usage")
    await interaction.response.send_message(embed=embed)


@tr_ai.command(name="on", description="Enable AI translation in this channel (translation must be ON)")
async def tr_ai_on(interaction: discord.Interaction):
    if interaction.channel_id not in state.active_channels:
        await interaction.response.send_message(
            embed=notice("⚠️ Enable translation first with `/tr on`.", COLOR_WARN), ephemeral=True
        )
        return
    state.ai_channels.add(interaction.channel_id)
    state.save()
    await update_presence(interaction.client)
    await interaction.response.send_message(
        embed=notice("🤖 AI translation **enabled** in this channel.", COLOR_OK)
    )


@tr_ai.command(name="off", description="Disable AI translation (switch back to Google Translate)")
async def tr_ai_off(interaction: discord.Interaction):
    state.ai_channels.discard(interaction.channel_id)
    state.save()
    await update_presence(interaction.client)
    await interaction.response.send_message(embed=notice("🔄 Switched back to **Google Translate**."))
