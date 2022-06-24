import discord
from discord.ext.commands import Context
import discord.ext.commands as commands

import random

from module.translation import translate_google

@commands.command()
async def 번역(ctx: Context, *, text: str):
    """구글 번역 api를 이용해 한국어를 영어로 번역합니다."""
    await ctx.channel.send(translate_google(text, "ko", "en"))

position = ["main 🛡️", "sub 🛡️", "main ⚔️", "sub ⚔️", "main 💉", "sub 💉"]

@commands.command()
async def 랜덤포지션(ctx: Context, *, text:str):
    """
    6명의 오버워치 포지션을 랜덤으로 결정합니다.
    """
    try:
        users = text.split()
        if len(users) < 6:
            while len(users) < 6:
                users.append(str(len(users)+1))
        random.shuffle(users)
        message = ""
        for pos, user in zip(position, users):
            message += pos + " = " + user + "\n"
        await ctx.channel.send(message)
    except:
        await ctx.channel.send("다시 시도해보라냥")


etcCmd = [ 번역, 랜덤포지션 ]