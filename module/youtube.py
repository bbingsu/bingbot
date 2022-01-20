import youtube_dl
from urllib.parse import urlencode, urljoin
from urllib.request import Request, urlopen
import json
import asyncio

API_URL = 'https://www.googleapis.com/youtube/v3/'

# - secrets.json에서 필요한 데이터를 가져옴
f = open('secrets.json', 'r')
# - 사용할 수 있는 형태로 바꿈(딕셔너리)
secrets = json.load(f)
# - secrets.json의 'youtube_api' 키의 value를 가져옴
# youtube data api에 접근하기 위해 사용됨
_youtubeKey = secrets['youtube_api']
f.close()

# - 모든 api 요청에 공통적으로 사용될 query
basicQuery = {
    'key': _youtubeKey
}

def ytSearch(searchString: str):
    '''
    들어온 string으로 유튜브에서 검색한 데이터를 리턴함
    '''

    # - api로 요청될 query를 만듬
    searchQueryDict = {
        **basicQuery,
        'part': 'snippet',
        'q': searchString,
        "type": "video"
    }
    # - 요청할 api url
    searchBaseUrl = urljoin(API_URL, 'search')
    # - 딕셔너리를 url 형식에 맞게 변경 
    # -> &part=snippet&q=%EC%B9%B4%EC%B9%B4%EC%98%A4...
    searchQuery = urlencode(searchQueryDict)
    # - 위의 두 부분을 합친 url. 실제 요청에 사용됨 
    searchUrl = searchBaseUrl + '?' + searchQuery

    # - 요청
    request = Request(searchUrl) 
    response =  urlopen(request)
    # - 응답 & json 형식으로 변경
    data = json.loads(response.read().decode())

    # - 추출
    # 들어온 검색 데이터에서 필요한 것들만 모아 새로운 리스트를 만들어 리턴함 
    results = list(map(lambda item: {
        "videoId": item['id']['videoId'],
        "title": item['snippet']['title'],
        "description": item['snippet']['description'],
        "thumbnail": item['snippet']['thumbnails']['default']['url']
    }, data['items']))
    return results 


async def getYoutubeVideoInfo(url: str):
    '''
    유튜브 영상 url를 받아 그 것의 audio url을 리턴함.
    '''
    ydlOptions = {
        'format': 'bestaudio/best',
        'noplaylist': True,
        'nocheckcertificate': True,
        'ignoreerrors': False,
        'quiet': True,
        'no_warnings': True,
        'default_search': 'auto',
    }
    
    try:
        with youtube_dl.YoutubeDL(ydlOptions) as ydl:
            loop = asyncio.get_event_loop()
            info = await loop.run_in_executor(None, lambda: ydl.extract_info(url, download=False))
            return {
                "audioUrl": info['url'],
                "title": info['title']
            }
    except:
        print("유튜브 오디오 링크를 얻는 중 오류가 발생했습니다.")

def isYoutubeVideoUrl(url: str) -> bool:
    '''
    유튜브 영상 url인지 확인함.
    '''
    return 'youtube' in url or 'youtu.be' in url

def getYoutubeVideoId(url: str) -> str:
    '''
    유튜브 영상 url을 받아 그 것의 video id를 리턴함.
    '''
    ydlOptions = {
        'format': 'bestaudio/best',
        'noplaylist': True,
        'nocheckcertificate': True,
        'ignoreerrors': False,
        'quiet': True,
        'no_warnings': True,
        'default_search': 'auto',
    }
    
    try:
        with youtube_dl.YoutubeDL(ydlOptions) as ydl:
            info = ydl.extract_info(url, download=False)
            return info['id']
    except:
        print("유튜브 오디오 ID를 얻는 중 오류가 발생했습니다.")

def getYoutubeTitle(videioID: str) -> str:
    '''
    유튜브 id 또는 url을 받아 그 것의 title을 리턴함.
    '''
    if isYoutubeVideoUrl(videioID):
        videioID = getYoutubeVideoId(videioID)

    params = {"format": "json", "url": "https://www.youtube.com/watch?v=%s" % videioID}
    url = "https://www.youtube.com/oembed"
    query_string = urlencode(params)
    url = url + "?" + query_string

    with urlopen(url) as response:
        response_text = response.read()
        data = json.loads(response_text.decode())
        return data['title']