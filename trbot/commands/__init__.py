"""슬래시 커맨드.

  translation  /tr on | off | status | topic | credits, /tr ai on | off
  tools        /tr summary, /tr math, ふりがな (메시지 우클릭 메뉴)
  roles        /genshin
"""
from discord import app_commands

from . import roles, tools, translation


def register(tree: app_commands.CommandTree):
    tree.add_command(translation.tr)   # tools 의 /tr summary, /tr math 도 이 그룹에 들어 있다
    tree.add_command(tools.furigana_menu)
    tree.add_command(roles.genshin)
