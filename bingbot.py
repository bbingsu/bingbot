import discord
from discord.ext.commands import Bot, when_mentioned_or, CommandNotFound

from cmd.basic import basicCmd
from cmd.game import gameCmd
from cmd.music import musicCmd
from cmd.etc import etcCmd

DEBUG = True

f = open("token.txt", 'r')
_token = f.read().splitlines()
f.close()

TOKEN = _token[0]       # deployment token
bot = Bot(command_prefix=when_mentioned_or('빙수 '))

if DEBUG:
    TOKEN = _token[1]   # development token
    bot = Bot(command_prefix='!')

@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online, activity=discord.Game('빙수 자기소개 | 그루밍'))
    print('[알림][빙수가 깨어 났어요.]')

@bot.event
async def on_message(msg: discord.Message):
    if msg.author.bot: return None
    await bot.process_commands(msg)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        await ctx.send('무슨 말인지 잘 모르겠다냥.. 이건 어떠냥?\n`빙수 자기소개`')
        return
    raise error

def main():
    for _cmd in basicCmd+gameCmd+musicCmd+etcCmd:
        bot.add_command(_cmd)
    bot.run(TOKEN)

if __name__ == '__main__':
    main()
