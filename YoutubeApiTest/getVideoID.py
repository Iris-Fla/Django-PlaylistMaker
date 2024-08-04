import re
from apiclient.discovery import build
import os
from dotenv import load_dotenv
import sqlite3

load_dotenv()
YOUTUBE_API_KEY = os.environ['YoutubeAPIKey']
youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

database = "database.db"

# urlから動画情報を取得
def extract_video_info(url):
    conn = sqlite3.connect(database)
    cur = conn.cursor()
    
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
            image = snipeetInfo['thumbnails']['default']['url']
            channeltitle = snipeetInfo['channelTitle']
            viwecount = staticsInfo['viewCount']
            publishedAt = snipeetInfo['publishedAt']
            link = f"https://www.youtube.com/watch?v={match.group(1)}"
            print(f"再生回数: {viwecount}")
            print(f"タイトル: {title}")
            print(f"チャンネル名: {channeltitle}")
            print(f"サムネイル: {image}")
            print(f"公開日: {publishedAt}")
            print(f"リンク: {link}")
            
            cur.execute('INSERT INTO videos values(?,?,?,?,?,?)',(title,channeltitle,image,link,viwecount,publishedAt))
            conn.commit()
            return
    return print('URLが正しくないかも')



if __name__ == '__main__':
    input_url = input('YouTubeのURLをはりつけてみて: ')
    extract_video_info(input_url)
