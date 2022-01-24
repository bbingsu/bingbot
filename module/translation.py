import json
from urllib.parse import urlencode
from urllib.request import urlopen

def translate_google(text, source, target):
    url = 'https://translate.google.com/translate_a/single'
    params = {
        'client': 'gtx',
        'sl': source,
        'tl': target,
        'dt': 't',
        'q': text
    }
    response = urlopen(url, urlencode(params).encode())
    result = json.loads(response.read().decode())
    return result[0][0][0]
