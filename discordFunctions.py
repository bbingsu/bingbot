import asyncio
import discord
from discord.ext.commands import Context
from collections import deque
from youtube import getYoutubeVideoInfo, getYoutubeTitle

#- 음악 리스트
musicQueue = deque()
# - 플레이 제어
event = asyncio.Event()

def addMusicQueue(url):
    musicQueue.append(url)

def listMusicQueue():
    return map(lambda element: element, musicQueue) 


async def playMusic(ctx: Context):
    '''
    musicQueue에서 링크를 가져와 재생함
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
