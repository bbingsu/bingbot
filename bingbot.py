import asyncio
import discord
from discord.ext.commands import Bot, Context
import random
from constants import *
from youtube import ytSearch, getYoutubeAudioUrl

f = open("token.txt", 'r')
_token = f.read().splitlines()
f.close()
TOKEN = _token[0]   # discord bot token

bot: Bot = Bot(command_prefix='!')


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
    embed = discord.Embed(title='',
                          description='')
    embed.set_image(url='https://raw.githubusercontent.com/bbingsu/bingbot/main/image/bingsu_default.jpeg')
    embed.set_footer(text='먀옹')
    await ctx.channel.send(embed=embed)


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
    winning, max_winning = 0, 0
    def _make_embed(description: str, before_dice: str):
        embed = discord.Embed(title='홀, 짝중에 하나를 선택해 주세요.',
                                description=description)
        embed.add_field(name='> 주사위의 눈', value=before_dice)
        embed.add_field(name='> 홀수', value='🌞')
        embed.add_field(name='> 짝수', value='🌝')
        embed.add_field(name='> 연승횟수', value=str(winning))
        return embed

    embed = _make_embed(even_odd_msg[INIT], '???')
    msg: discord.Message = await ctx.channel.send(embed=embed)
    await msg.add_reaction('🌞')
    await msg.add_reaction('🌝')

    def _check(reaction: discord.reaction.Reaction, user: discord.member.Member):
        return str(reaction) in ['🌞', '🌝'] and \
                user == ctx.author and \
                reaction.message.id == msg.id
    try:
        while True:
            reaction, user = await bot.wait_for('reaction_add', check=_check, timeout=10)
            await msg.clear_reactions()

            # win
            if  (str(reaction) == '🌞' and dice % 2 == 1) or \
                (str(reaction) == '🌝' and dice % 2 == 0):
                winning += 1
                embed = _make_embed(even_odd_msg[WIN], str(dice))
            # lose
            else:
                winning = 0
                embed = _make_embed(even_odd_msg[LOSE], str(dice))

            await msg.edit(embed=embed)
            await msg.add_reaction('🌞')
            await msg.add_reaction('🌝')
            dice = random.randint(1, 6)
            max_winning = max(max_winning, winning)
    except Exception as e:
        await msg.clear_reactions()
    # print('[알림][홀짝 게임 종료]')
    # print('종료 유저 이름:', ctx.author)
    # print('최고 연승 횟수:', max_winning)
    await ctx.channel.send(ctx.author.__str__().split('#')[0] + '님, 최고 ' + str(max_winning) + '연승 달성!')

@bot.command()
async def 검색(ctx: Context, searchString: str):
    # - 유튜브 api로 검색한 데이터 가져옴
    ytList = ytSearch(searchString)

    # - 가져온 데이터를 활용해 embed로 표시함
    def ytDictToEmbed(ytDict):
        embed = discord.Embed(title=ytDict['title'], description=ytDict['description'], url=f"https://www.youtube.com/watch?v={ytDict['videoId']}")
        embed.set_thumbnail(url=ytDict['thumbnail'])
        return ctx.channel.send(embed=embed)       

    # - 동시에 실행...이긴 한데?
    # 제대로 안되는 걸 보니 먼가먼가 잘못됨
    await asyncio.gather(*[ytDictToEmbed(ytDict) for ytDict in ytList])


@bot.command()
async def 입장(ctx: Context):
    """
    음성 채팅에 봇을 참여시킴
    """

    author = ctx.message.author

    # - voice 채널 접근
    if not author.voice:
        await ctx.channel.send(f"{author.name} 집사는 보이스 채널이나 들어가고 오라냥") 
    else:
        await author.voice.channel.connect()
        await ctx.channel.send("연결됐다냥")


@bot.command()
async def 퇴장(ctx: Context):
    author = ctx.message.author
    voiceClient = ctx.voice_client

    # - 봇이 보이스 채널에 연결되어 있는지 확인 후 연결 해제
    if voiceClient != None:
        if voiceClient.is_connected():
            await voiceClient.disconnect()
    else:
        await ctx.channel.send("아직 들어가지도 않았다냥")


@bot.command()
async def 플레이(ctx: Context, toPlay):
    # - 유튜브 오디오 링크
    audioUrl = getYoutubeAudioUrl(toPlay)
    # - 봇이 입장한 보이스 채널
    voiceClient = ctx.voice_client

    # - 봇이 보이스 채널에 있는지 확인한 다음 음원을 재생함
    if voiceClient != None:
        try:
            # - 음원을 재생 가능한 형태로
            voiceSource = discord.FFmpegPCMAudio(source=audioUrl, executable="ffmpeg")
            # - 음원 재생
            voiceClient.play(voiceSource)
            # - 재생 안내
            await ctx.channel.send(f"지금은 {toPlay}를 재생하고 있다냥")
        except:
            await ctx.channel.send(f"{toPlay}는 재생할 수 없다냥")
    # - 봇이 보이스채널에 들어가 있지 않을 때
    else:
        await ctx.channel.send("나보다 약한 녀석의 말은 듣지 않는다옹")


bot.run(TOKEN)