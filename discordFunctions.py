import asyncio
import discord
from discord.ext.commands import Context
from collections import deque
from youtube import getYoutubeVideoInfo

#- 음악 리스트, deprecated
musicQueue = deque()
# - 플레이 제어, deprecated
event = asyncio.Event()

def addMusicQueue(url):
    musicQueue.append(url)

def listMusicQueue():
    return map(lambda element: element, musicQueue) 


async def deprecated_playMusic(ctx: Context):
    '''
    musicQueue에서 링크를 가져와 재생함

    사용하지 않음. 기능이 과도해 다이어트 들어감. 새로운 `playMusic()`을 사용하세용~~~
    '''

    # - 봇이 보이스 채널에 있는지 확인한 다음 음원을 재생함
    voiceClient = ctx.voice_client
    if voiceClient != None:
        try:
            while True:
                # while의 탈출 조건, 큐의 재생이 끝나면 ㄱㄱ
                if not musicQueue:
                    await ctx.channel.send("리스트에 있는 음악을 전부 재생했다냥!")
                    return;
                # - 재생에 필요한 정보들 가져오기
                videoUrl = musicQueue.popleft() 
                videoInfo = await getYoutubeVideoInfo(videoUrl)
                audioUrl = videoInfo['audioUrl']
                title = videoInfo['title']
                # - 이벤트를 초기화 함, False
                event.clear()
                # - 음원을 재생 가능한 형태로
                voiceSource = discord.FFmpegPCMAudio(source=audioUrl, executable="ffmpeg")
                # - 음원 재생
                # after에 들어있는 함수는 음원 재생이 끝나면 실행됨. 이벤트를 True로 만들어 줘 다음 곡의 재생이 가능토록 함.
                voiceClient.play(source=voiceSource, after=lambda _: event.set())
                # - 재생 안내
                await ctx.channel.send(f"지금은 '{title}' 를 재생하고 있다냥")
                # - 이벤트가 True로 바뀔 때까지 개같이 대기, False
                await event.wait()

        except:
            await ctx.channel.send(f" '{title}' 는 재생할 수 없다냥")
    # - 봇이 보이스채널에 들어가 있지 않을 때
    else:
        await ctx.channel.send("나보다 약한 녀석의 말은 듣지 않는다옹")

async def playMusic(ctx: Context, videoUrl: str):
    '''
    들어온 링크를 재생함.

    기존 `playMusic()`은 이름과 달리 담당하는 기능이 많았음.
    기능을 줄여 인자로 들어오는 음원만 재생하게 만듬.
    '''

    # - 음원이 재생 중일 때 앱의 흐름을 멈추는 역할을 함
    isPlayingEvent = asyncio.Event()

    # - 봇이 보이스 채널에 있는지 확인한 다음 음원을 재생함
    voiceClient = ctx.voice_client
    if voiceClient != None:
        try:
            # - 재생에 필요한 정보들 가져오기
            videoInfo = await getYoutubeVideoInfo(videoUrl)
            audioUrl = videoInfo['audioUrl']
            title = videoInfo['title']
            # - 음원을 재생 가능한 형태로
            voiceSource = discord.FFmpegPCMAudio(source=audioUrl, executable="ffmpeg")
            # - 음원 재생
            # after에 들어있는 함수는 음원 재생이 끝나면 실행됨. 이벤트를 True로 만들어 줘 다음 곡의 재생이 가능토록 함.
            voiceClient.play(source=voiceSource, after=lambda _: isPlayingEvent.set())
            # - 재생 안내
            await ctx.channel.send(f"지금은 '{title}' 를 재생하고 있다냥")
            # - 이벤트가 True로 바뀔 때까지 개같이 대기, False
            await isPlayingEvent.wait()

        except:
            await ctx.channel.send(f" '{title}' 는 재생할 수 없다냥")
    # - 봇이 보이스채널에 들어가 있지 않을 때
    else:
        await ctx.channel.send("나보다 약한 녀석의 말은 듣지 않는다옹")
