"""역할 받기 커맨드."""
import logging

import discord
from discord import app_commands

from ..config import COLOR_ERROR, COLOR_OK, ROLE_GENSHIN
from ..ui import notice

log = logging.getLogger(__name__)


# 원신 채널 역할을 받는다. 이미 있으면 뺀다. 결과는 누른 사람에게만 보인다
@app_commands.command(name="genshin", description="원신 채널 역할 받기/빼기 · 原神チャンネルのロールを付ける/外す")
async def genshin(interaction: discord.Interaction):
    role = interaction.guild.get_role(ROLE_GENSHIN) if interaction.guild else None
    if role is None:
        await interaction.response.send_message(
            embed=notice("❌ Role not found. (check ROLE_GENSHIN)", COLOR_ERROR), ephemeral=True
        )
        return

    member = interaction.user
    try:
        if role in member.roles:
            await member.remove_roles(role, reason="/genshin")
            embed = notice(f"➖ {role.mention} 역할을 뺐어요.\n➖ {role.mention} ロールを外しました。")
        else:
            await member.add_roles(role, reason="/genshin")
            embed = notice(f"✅ {role.mention} 역할을 받았어요.\n✅ {role.mention} ロールを付けました。", COLOR_OK)
    except discord.Forbidden:
        # 봇에 '역할 관리' 권한이 없거나, 봇 역할이 이 역할보다 아래에 있다
        log.error("cannot change role %s: missing Manage Roles, or the role is above the bot's role", role.name)
        embed = notice(
            "❌ 봇이 이 역할을 줄 수 없어요. 관리자에게 알려주세요.\n"
            "❌ ボットがこのロールを付けられません。管理者に連絡してください。",
            COLOR_ERROR,
        )
    await interaction.response.send_message(embed=embed, ephemeral=True)
