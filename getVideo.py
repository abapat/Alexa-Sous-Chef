import urllib
import requests
import defines

Base_Url = "https://www.googleapis.com/youtube/v3/search"

def main():
    url = get_video("diceanonion")
    print url    

def get_video(query):
    params = {'part': 'id', 'q': query, 'type': 'video', 'key': defines.API_key}
    url = Base_Url + "?" + urllib.urlencode(params)
    response = requests.get(url)
    youtube_id = response.json()['items'][0]['id']['videoId']
    return "https://www.youtube.com/watch?v=" + youtube_id


if __name__ == "__main__":
    main()
