import discord
from discord.ext import commands
from discord.ext.commands import Bot, Context
import random
# utils.py
from utils import getImagePath

f = open("token.txt", 'r')
_token = f.read().splitlines()
f.close()
TOKEN = _token[0]   # discord bot token

bot: Bot = commands.Bot(command_prefix='!')


@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online, activity=discord.Game('!소개 그루밍'))
    print('[알림][빙수가 깨어 났어요.]')


@bot.event
async def on_message(msg: discord.Message):
    if msg.author.bot: return None
    await bot.process_commands(msg)


@bot.command()
async def 안녕(ctx: Context):
    await ctx.channel.send('야옹')


@bot.command()
async def 바보(ctx: Context):
    await ctx.channel.send('니가 더')


@bot.command()
async def 이몸등장(ctx: Context):
    try:
        # discord.File을 통해 이미지를 가져온 후 디스코드에 전송함
        # 다만, 이미지와 같은 파일을 보낼 때는 file을 사용해야 함
        await ctx.channel.send(file=discord.File(getImagePath('bingsu_default.jpeg')))
        await ctx.channel.send('먀옹')
    except:
        pass


@bot.command()
async def 소개(ctx: Context):
    embed = discord.Embed(title='저는 빙수에요',
                          description='이렇게 사용해요!')
    embed.add_field(name='대화', value='!안녕\r\n!바보')
    embed.add_field(name='게임', value='!홀짝')
    embed.add_field(name='사진', value='!이몸등장\r\n\!랜덤')
    embed.set_thumbnail(url='https://raw.githubusercontent.com/bbingsu/bingbot/main/image/merry.jpg')
    embed.set_footer(text='열심히 만드는 중임')
    await ctx.channel.send(embed=embed)


@bot.command()
async def 홀짝(ctx: Context):
    dice = random.randint(1, 6)
    winning = 0
    embed = discord.Embed(title='홀, 짝중에 하나를 선택해 주세요.',
                          description='선택 한 뒤에 어떤 수가 나왔나 알려 드려요.')
    embed.add_field(name='> 주사위의 눈', value='???')
    embed.add_field(name='> 홀수', value='🌞')
    embed.add_field(name='> 짝수', value='🌝:')
    embed.add_field(name='> 연승횟수', value=str(winning))
    await ctx.message.delete()
    msg: discord.Message = await ctx.channel.send(embed=embed)
    await msg.add_reaction('🌞')
    await msg.add_reaction('🌝')

    def check(reaction, user):
            return str(reaction) in ['🌞', '🌝'] and \
            user == ctx.author and reaction.message.id == msg.id
    
    while True:
        try:
            reaction, user = await bot.wait_for('reaction_add', check=check)
            await msg.clear_reactions()
            if  (str(reaction) == '🌞' and dice % 2 == 1) or \
                (str(reaction) == '🌝' and dice % 2 == 0):
                embed = discord.Embed(title='홀, 짝중에 하나를 선택해 주세요.',
                                    description='정답입니다! 계속해서 도전해보세요!')
                winning += 1
            else:
                embed = discord.Embed(title='홀 짝중에 하나를 선택해 주세요.',
                                    description='틀렸네요... 계속 도전해 보세요!')
                winning = 0
            
            embed.add_field(name='> 주사위의 눈', value=str(dice))
            embed.add_field(name='> 홀수', value='🌞')
            embed.add_field(name='> 짝수', value='🌝')
            embed.add_field(name='> 연승횟수', value=str(winning))

            await msg.edit(embed=embed)
            await msg.add_reaction('🌞')
            await msg.add_reaction('🌝')
            dice = random.randint(1, 6)
            print(dice)
        except: pass



bot.run(TOKEN)