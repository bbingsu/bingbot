import discord
from discord.ext.commands import Bot

from cmd.basics import *
from cmd.game import *
from cmd.musics import *

DEBUG = True

f = open("token.txt", 'r')
_token = f.read().splitlines()
f.close()

TOKEN = _token[0]   # discord bot token
bot: Bot = Bot(command_prefix='!')

if DEBUG:
    TOKEN = _token[1]
    bot: Bot = Bot(command_prefix='!!')

@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online, activity=discord.Game('!소개 그루밍'))
    print('[알림][빙수가 깨어 났어요.]')

@bot.event
async def on_message(msg: discord.Message):
    if msg.author.bot: return None
    await bot.process_commands(msg)

basicCmd = [ 안녕, 바보 ]
gameCmd = [ 홀짝 ]
musicCmd = [ 검색, 입장, 퇴장, 틀어, 멈춰, 예약목록 ]

def main():
    for _cmd in basicCmd+gameCmd+musicCmd:
        bot.add_command(_cmd)
    bot.run(TOKEN)

if __name__ == '__main__':
    main()
