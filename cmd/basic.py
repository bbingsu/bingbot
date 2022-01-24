import discord
from discord.ext.commands import Context
import discord.ext.commands as commands


@commands.command()
async def 안녕(ctx: Context):
    await ctx.channel.send('야옹')

@commands.command()
async def 바보(ctx: Context):
    await ctx.channel.send('니가 더')

@commands.command()
async def 기여(ctx: Context):
    await ctx.channel.send('기여해 주세요! https://github.com/bbingsu/bingbot')

@commands.command()
async def 이몸등장(ctx: Context):
    embed = discord.Embed(title='',
                          description='')
    embed.set_image(url='https://raw.githubusercontent.com/bbingsu/bingbot/main/image/bingsu_default.jpeg')
    embed.set_footer(text='먀옹')
    await ctx.channel.send(embed=embed)

introduce = discord.Embed(title='나는 빙수다냥',
                          description="이렇게 사용한다냥!\n`빙수 안녕`, `@BINGSU 안녕`")
introduce.add_field(name='대화', value='안녕\r\n바보\r\n기여')
introduce.add_field(name='게임', value='홀짝')
introduce.add_field(name='사진', value='이몸등장\r\n\랜덤')
introduce.add_field(name='노래', value='입장\r\n\틀어\r\n\멈춰\r\n\퇴장')
introduce.add_field(name='기타', value='번역')
introduce.set_thumbnail(url='https://raw.githubusercontent.com/bbingsu/bingbot/main/image/merry.jpg')
introduce.set_footer(text='명령어 아이디어 제공은 환영한다냥!')

@commands.command()
async def 소개(ctx: Context):
    await ctx.channel.send(embed=introduce)

@commands.command()
async def 소개해봐(ctx: Context):
    await ctx.channel.send(embed=introduce)

@commands.command()
async def 자기소개(ctx: Context):
    await ctx.channel.send(embed=introduce)

basicCmd = [ 안녕, 바보, 기여, 이몸등장, 소개, 소개해봐, 자기소개 ]