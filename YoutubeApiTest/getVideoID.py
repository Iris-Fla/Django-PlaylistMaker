import re
from apiclient.discovery import build
import os
from dotenv import load_dotenv

load_dotenv()

YOUTUBE_API_KEY = os.environ['YoutubeAPIKey']

input_url = input('YouTubeのURLをはりつけてみて: ')

youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)




# urlから動画情報を取得
def extract_video_info(url):
    # YouTubeのURLパターン
    patterns = [
        r'(?:https?:\/\/)?(?:www\.)?youtube\.com\/watch\?v=([^&]+)',
        r'(?:https?:\/\/)?(?:www\.)?youtu\.be\/([^?]+)',
        r'(?:https?:\/\/)?(?:www\.)?youtube\.com\/embed\/([^?]+)'
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            videos_response = youtube.videos().list(
                part='snippet,statistics',
                id='{},'.format(match.group(1))
                ).execute()
            snipeetInfo = videos_response["items"][0]["snippet"]
            staticsInfo = videos_response["items"][0]["statistics"]
            title = snipeetInfo['title']
            channeltitle = snipeetInfo['channelTitle']
            viwecount = staticsInfo['viewCount']
            print(f"再生回数: {viwecount}")
            print(f"タイトル: {title}")
            print(f"チャンネル名: {channeltitle}")
            return
    return print('URLが正しくないかも')

extract_video_info(input_url)