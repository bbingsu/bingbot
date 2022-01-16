import asyncio
from collections import deque

from discord import player
from discordFunctions import addMusicQueue, listMusicQueue, playMusic
import discord
from discord.ext.commands import Bot, Context
import random
from constants import *
from youtube import *

f = open("token.txt", 'r')
_token = f.read().splitlines()
f.close()
TOKEN = _token[0]   # discord bot token

bot: Bot = Bot(command_prefix='!')

# - 채널별 음원 예약목록
musicDict = dict()


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
    embed.add_field(name='노래', value='!입장\r\n\!틀어\r\n\!멈춰\r\n\!퇴장')
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
    await ctx.channel.send(ctx.author.name + '님, 최고 ' + str(max_winning) + '연승 달성!')


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
async def 틀어(ctx: Context, url: str):
    async def playMusics(musicDeque: deque):
        '''
        들어온 deque가 빌 때까지 음악을 재생함

        모든 목록을 재생했다면 True를 리턴함.

        기존 `playMusic()`의 예약목록 음원 재생 기능을 계승함.

        파이썬은 들어온 함수의 인자가 변경 가능한 것(mutable)이라면 참조를 가리킴.
        musicDeque가 외부에서 변경되면 그대로 변경된 값을 사용할 수 있다는 것!!
        '''

        # - 예약목록에 음원이 없다면 재귀를 종료
        if musicDeque:
            # - 음원 재생, 재생이 끝날 때까지 기다림
            await playMusic(ctx, musicDeque.popleft())
            # - 예약목록 상태 출력
            print("[playMusics > deque]", musicDeque)
            # - 재귀, 재생할 예약목록을 인자로 받음
            # javascript와는 달리 리턴 때도 await를 붙여줘야 함.
            return await playMusics(musicDeque) 
        # - 예약목록의 모든 음원의 재생을 끝낸다면 True를 리턴하며 함수를 빠져나감
        else: 
            return True 

    # - 봇이 연결된 보이스 채널
    voiceClient = ctx.voice_client
    # - 명령어를 입력한 유저가 속한 채널의 id
    guildId = ctx.author.guild.id 

    # - 해당 채널에 예약목록이 존재한다면 url을 추가, 그렇지 않다면 새로운 deque를 생성하며 url을 추가
    if guildId in musicDict:
        musicDict[guildId].append(url)
    else:
        musicDict[guildId] = deque([url])
    await ctx.channel.send('예약했다냥!')

    # - 음원이 재생되지 않고 있다면 실행
    if(not voiceClient.is_playing()):
        # - 채널 아이디에 맞는 예약목록의 음원 재생 시작
        playResult = await playMusics(musicDict[guildId])
        # - 예약목록의 재생이 끝났다면 안내 메세지 출력
        if playResult:
            await ctx.channel.send('예약목록에 있는 음악의 재생을 모두 완료했다냥!') 


@bot.command()
async def 멈춰(ctx: Context):
    voiceClient = ctx.voice_client
    if voiceClient != None:
        if voiceClient.is_playing():
            try:
                await voiceClient.stop()
            except Exception as e:
                pass
            await ctx.channel.send("재생을 중지하였다냥")
        else:
            await ctx.channel.send('이미 중지 되었다냥')
    else:
        await ctx.channel.send('아직 들어가지도 않았다냥')


@bot.command()
async def 예약목록(ctx: Context):
    # - 명령어를 입력한 유저가 속한 채널의 아이디
    guildId = ctx.author.guild.id
    # - 채널에 예약목록이 존재한다면 출력, 아님 예외 메세지 출력
    if guildId in musicDict and musicDict[guildId]:
        for element in musicDict[guildId]:
            await ctx.channel.send(element)
    else:
        await ctx.channel.send("예약된 노래가 없다냥!")

bot.run(TOKEN)
