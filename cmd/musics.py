import discord
from discord.ext.commands import Context
from discord.ext import commands

import asyncio
from collections import deque

from module.youtube import *
from module.discordFunctions import getMembersChannelId, playMusic

# - 채널별 보이스 클라이언트 및 음원 예약목록
# 구조는 아래와 같음
# { key: {'voice': VoiceClient, 'list': deque([...url])}}
musicDict = dict()

@commands.command()
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


@commands.command()
async def 입장(ctx: Context):
    """
    음성 채팅에 봇을 참여시킴
    """

    # - 명령어를 실행한 유저
    author = ctx.message.author
    # - 명령어를 실행한 유저가 속한 채널의 아이디
    channelId = getMembersChannelId(ctx)

    # - voice 채널 접근
    if not author.voice:
        await ctx.channel.send(f"{author.name} 집사는 보이스 채널이나 들어가고 오라냥") 
    else:
        # - 반환된 보이스 프로토콜. 봇을 보이스 채널에서 disconnect할 때 사용됨
        voiceProtocol = await author.voice.channel.connect()
        musicDict[channelId] = {**musicDict, "voice": voiceProtocol}
        await ctx.channel.send("연결됐다냥")


@commands.command()
async def 퇴장(ctx: Context):
    channelId = getMembersChannelId(ctx)
    voiceClient = musicDict[channelId]['voice']

    # - 봇이 보이스 채널에 연결되어 있는지 확인 후 연결 해제
    if voiceClient != None:
        if voiceClient.is_connected():
            await voiceClient.disconnect()
    else:
        await ctx.channel.send("아직 들어가지도 않았다냥")


@commands.command()
async def 틀어(ctx: Context, url: str):
    async def playMusics(musicDict: dict):
        '''
        들어온 deque가 빌 때까지 음악을 재생함

        모든 목록을 재생했다면 True를 리턴. 예외가 발생했을 시는 False 리턴.

        기존 `playMusic()`의 예약목록 음원 재생 기능을 계승함.

        파이썬은 들어온 함수의 인자가 변경 가능한 것(mutable)이라면 참조를 가리킴.
        musicDeque가 외부에서 변경되면 그대로 변경된 값을 사용할 수 있다는 것!!
        '''

        # - 딕셔너리에서 필요한 것들을 추출
        musicDeque = musicDict['list']
        musicVoiceClient = musicDict['voice']

        # - 예약목록에 음원이 없다면 재귀를 종료
        try:
            if musicDeque:
                # - 음원 재생, 재생이 끝날 때까지 기다림
                await playMusic(ctx, musicVoiceClient, musicDeque.popleft())
                # - 예약목록 상태 출력
                print("[playMusics > deque]", musicDeque)
                # - 재귀, 재생할 예약목록을 인자로 받음
                # javascript와는 달리 리턴 때도 await를 붙여줘야 함.
                return await playMusics(musicDict) 
            # - 예약목록의 모든 음원의 재생을 끝낸다면 True를 리턴하며 함수를 빠져나감
            else: 
                return True 
        except:
            return False

    # - 명령어를 입력한 유저가 속한 채널의 id
    channelId = getMembersChannelId(ctx)

    # - 해당 채널에 예약목록이 존재한다면 url을 추가, 그렇지 않다면 새로운 deque를 생성하며 url을 추가
    if channelId in musicDict and 'list' in musicDict[channelId]:
        musicDict[channelId]['list'].append(url)
    else:
        musicDict[channelId] = {**musicDict[channelId], 'list': deque([url])}
    await ctx.channel.send('예약했다냥!')

    # - 음원이 재생되지 않고 있다면 실행
    # if(not voiceClient.is_playing()):
    if(not musicDict[channelId]['voice'].is_playing()):
        # - 채널 아이디에 맞는 예약목록의 음원 재생 시작
        playResult = await playMusics(musicDict[channelId])
        # - 예약목록의 재생이 끝났다면 안내 메세지 출력
        if playResult:
            await ctx.channel.send('예약목록에 있는 음악의 재생을 모두 완료했다냥!') 


@commands.command()
async def 멈춰(ctx: Context):
    # - musicDict에서 해당 채널에 연결된 보이스 클라이언트를 가져옴
    channelId = getMembersChannelId(ctx)
    voiceClient = musicDict[channelId]['voice']

    if voiceClient != None:
        if voiceClient.is_playing():
            try:
                await voiceClient.stop()
            except Exception as e:
                pass
            # - 해당 채널의 voiceClient를 비움
            voiceClient = None
            await ctx.channel.send("재생을 중지하였다냥")
        else:
            await ctx.channel.send('이미 중지 되었다냥')
    else:
        await ctx.channel.send('아직 들어가지도 않았다냥')


@commands.command()
async def 예약목록(ctx: Context):
    # - 명령어를 입력한 유저가 속한 채널의 아이디
    guildId = getMembersChannelId(ctx)
    # - 채널에 예약목록이 존재한다면 출력, 아님 예외 메세지 출력
    if guildId in musicDict and 'list' in musicDict[guildId]:
        for element in musicDict[guildId]['list']:
            await ctx.channel.send(element)
    else:
        await ctx.channel.send("예약된 노래가 없다냥!")