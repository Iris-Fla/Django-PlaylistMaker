import os
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from datetime import datetime, timezone

import os
from dotenv import load_dotenv

load_dotenv()

# YouTube Data API v3のAPIキー
API_KEY = os.environ['YoutubeAPIKey']

def get_youtube_playlist_info(url, max_results=50):
    def extract_playlist_id(url):
        if 'list=' in url:
            return url.split('list=')[1].split('&')[0]
        return None

    playlist_id = extract_playlist_id(url)
    if not playlist_id:
        return None, "プレイリストが見つかりませんでした"

    youtube = build('youtube', 'v3', developerKey=API_KEY)
    
    try:
        #videosには動画情報が格納される
        videos = []
        next_page_token = None
        
        while True:
            playlist_request = youtube.playlistItems().list(
                part="snippet,contentDetails",
                playlistId=playlist_id,
                maxResults=min(max_results, 50),
                pageToken=next_page_token
            )
            playlist_response = playlist_request.execute()
            
            video_ids = [item['contentDetails']['videoId'] for item in playlist_response['items']]
            
            video_request = youtube.videos().list(
                part="snippet,statistics",
                id=','.join(video_ids)
            )
            video_response = video_request.execute()
            
            for item in video_response['items']:
                snippet = item['snippet']
                statistics = item['statistics']
                
                video_info = {
                    'title': snippet['title'],
                    'channel': snippet['channelTitle'],
                    'image': snippet['thumbnails']['default']['url'],
                    'url': f"https://www.youtube.com/watch?v={item['id']}",
                    'views': int(statistics.get('viewCount', 0)),
                    'published_at': datetime.fromisoformat(snippet['publishedAt'].replace('Z', '+00:00')).replace(tzinfo=timezone.utc)
                }
                videos.append(video_info)
            
            next_page_token = playlist_response.get('nextPageToken')
            max_results -= 50
            
            if not next_page_token or max_results <= 0:
                break
        
        return videos, None
    
    except HttpError as e:
        return None, f"An HTTP error {e.resp.status} occurred: {e.content}"

# 実行側
def print_playlist_info(url):
    videos, error = get_youtube_playlist_info(url)
    if error:
        print(f"Error: {error}")
    elif videos:
        print(f"プレイリストURL: {url}")
        for i, video in enumerate(videos, 1):
            print(f"{i}. 動画タイトル: {video['title']}")
            print(f"   投稿者: {video['channel']}")
            print(f"   URL: {video['url']}")
            print(f"   サムネイル: {video['image']}")
            print(f"   視聴回数: {video['views']:,}")
            print(f"   投稿日: {video['published_at'].strftime('%Y-%m-%d')}")
            print()
    else:
        print("ビデオが見つかりませんでした")

if __name__ == '__main__':
    url = input('YouTubeのプレイリストURLをはりつけてみて: ')
    print_playlist_info(url)