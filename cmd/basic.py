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
async def 이몸등장(ctx: Context):
    embed = discord.Embed(title='',
                          description='')
    embed.set_image(url='https://raw.githubusercontent.com/bbingsu/bingbot/main/image/bingsu_default.jpeg')
    embed.set_footer(text='먀옹')
    await ctx.channel.send(embed=embed)

@commands.command()
async def 소개(ctx: Context):
    embed = discord.Embed(title='저는 빙수에요',
                          description='이렇게 사용해요!')
    embed.add_field(name='대화', value='!안녕\r\n!바보')
    embed.add_field(name='게임', value='!홀짝')
    embed.add_field(name='사진', value='!이몸등장\r\n\!랜덤')
    embed.add_field(name='노래', value='!입장\r\n\!틀어\r\n\!멈춰\r\n\!퇴장')
    embed.set_thumbnail(url='https://raw.githubusercontent.com/bbingsu/bingbot/main/image/merry.jpg')
    embed.set_footer(text='열심히 만드는 중임')
    await ctx.channel.send(embed=embed)

basicCmd = [ 안녕, 바보, 이몸등장, 소개 ]