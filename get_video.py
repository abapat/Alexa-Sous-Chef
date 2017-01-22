import urllib
import requests

Base_Url = "https://www.googleapis.com/youtube/v3/search"
API_key = "AIzaSyByWDjb6X-vSMGpN5pw5PhM1lmGnUCKcH4"

def get_video(query):
    params = {'part': 'id', 'q': query, 'type': 'video', 'key': API_key}
    url = Base_Url + "?" + urllib.urlencode(params)
    response = requests.get(url)
    youtube_id = response.json()['items'][0]['id']['videoId']
    return "https://www.youtube.com/watch?v=" + youtube_id

url = get_video("diceanonion")
print url


