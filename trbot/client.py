"""봇 본체."""
import logging

import discord
from discord import app_commands

from . import commands
from .config import GUILD, TOKEN
from .handler import handle_message
from .ui import update_presence

log = logging.getLogger(__name__)


class TranslatorBot(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        # 길드 커맨드로만 등록한다 (전역 커맨드는 반영이 느리다).
        # on_ready 와 달리 재접속 때마다 다시 실행되지 않는다
        commands.register(self.tree)
        self.tree.copy_global_to(guild=GUILD)
        synced = await self.tree.sync(guild=GUILD)
        log.info("Synced %d commands: %s", len(synced), ", ".join(f"/{c.name}" for c in synced))

    async def on_ready(self):
        log.info("Logged in as %s (servers: %s)", self.user, ", ".join(g.name for g in self.guilds))
        await update_presence(self)

    async def on_message(self, message: discord.Message):
        await handle_message(message)


def run():
    # root_logger=True: discord.py 의 로그 설정을 이 봇의 로거에도 적용한다
    TranslatorBot().run(TOKEN, root_logger=True)
