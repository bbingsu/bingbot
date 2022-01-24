import discord
from discord.ext.commands import Context
import discord.ext.commands as commands

from module.translation import translate_google

@commands.command()
async def 번역(ctx: Context, *, text: str):
    """구글 번역 api를 이용해 한국어를 영어로 번역합니다."""
    await ctx.channel.send(translate_google(text, "ko", "en"))

etcCmd = [ 번역 ]