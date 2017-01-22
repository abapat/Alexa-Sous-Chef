import re
import httplib, urllib, base64
import defines


def getThumbnail(title):
    params = urllib.urlencode({
        # Request parameters
        'q': title,
        'count': '1',
        'offset': '0',
        'mkt': 'en-us',
        'safeSearch': 'Moderate',
    })

    try:
        conn = httplib.HTTPSConnection('api.cognitive.microsoft.com')
        conn.request("GET", "/bing/v5.0/images/search?%s" % params, "{body}", defines.headers)
        response = conn.getresponse()
        data = response.read()
        res = re.findall('"thumbnailUrl": "(.*?)"', data)
        conn.close()
        if res == None:
            return None
        return res[0]
    except Exception as e:
        print(e)
