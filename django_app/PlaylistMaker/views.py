import re
import os
from googleapiclient.discovery import build
from django.shortcuts import render,redirect
from django.conf import settings
from .models import video_info
from django.utils.dateparse import parse_datetime
from .forms import VideoSelectionForm
import google_auth_oauthlib.flow
import googleapiclient.discovery
# Create your views here.

SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]
API_SERVICE_NAME = "youtube"
API_VERSION = "v3"

def index(request):
  videos = video_info.objects.all()
  if request.method == 'POST':
        form = VideoSelectionForm(request.POST)
        if form.is_valid():
            for video in videos:
                video.is_selected = request.POST.get(f'video_{video.id}', False) == 'on'
                video.save()
            return redirect('selected_videos')
        return render(request, 'PlaylistMaker/selected_videos.html', {'videos': selected_videos})
  return render(request, 'PlaylistMaker/index.html', {'videos': videos})

def get_authenticated_service():
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(settings.CLIENT_SECRETS_FILE, SCOPES)
    credentials = flow.run_local_server(port=0)
    return googleapiclient.discovery.build(API_SERVICE_NAME, API_VERSION, credentials=credentials)

def create_youtube_playlist(request):
    selected_videos = video_info.objects.filter(is_selected=True)
    video_ids = [video.videoid for video in selected_videos]

    if request.method == 'POST':
        playlist_name = request.POST.get('playlist_name')
        if playlist_name:
            youtube = get_authenticated_service()
            
            # プレイリストを作成
            playlist_response = youtube.playlists().insert(
                part="snippet,status",
                body={
                    "snippet": {
                        "title": playlist_name,
                        "description": "A playlist created with selected videos",
                        "tags": ["sample playlist", "API call"],
                        "defaultLanguage": "en"
                    },
                    "status": {
                        "privacyStatus": "private"
                    }
                }
            ).execute()

            playlist_id = playlist_response['id']

            # プレイリストに動画を追加
            for video_id in video_ids:
                youtube.playlistItems().insert(
                    part="snippet",
                    body={
                        "snippet": {
                            "playlistId": playlist_id,
                            "resourceId": {
                                "kind": "youtube#video",
                                "videoId": video_id
                            }
                        }
                    }
                ).execute()

            return redirect('index')

    return render(request, 'PlaylistMaker/create_playlist.html', {'videos': selected_videos})


def create(request):
    if request.method == 'POST':
        url = request.POST.get('url')
        youtube = build('youtube', 'v3', developerKey=settings.YOUTUBE_API_KEY)
        
        # プレイリストIDを抽出するパターンを追加
        patterns = [
            r'(?:https?:\/\/)?(?:www\.)?youtube\.com\/watch\?v=([^&]+)',
            r'(?:https?:\/\/)?(?:www\.)?youtu\.be\/([^?]+)',
            r'(?:https?:\/\/)?(?:www\.)?youtube\.com\/embed\/([^?]+)',
            r'(?:https?:\/\/)?(?:www\.)?youtube\.com\/playlist\?list=([^&]+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                if 'playlist' in pattern:
                    # プレイリストの場合
                    playlist_id = match.group(1)
                    videos = get_playlist_videos(youtube, playlist_id)
                else:
                    # 単一の動画の場合
                    video_id = match.group(1)
                    videos = [get_video_info(youtube, video_id)]
                
                created_videos = []
                for video in videos:
                    if video:
                        video_obj, created = video_info.objects.update_or_create(
                            videoid=video['id'],
                            defaults={
                                'title': video['title'],
                                'channel': video['channel'],
                                'image': video['image'],
                                'url': f"https://www.youtube.com/watch?v={video['id']}",
                                'views': video['views'],
                                'published_date': video['published_date']
                            }
                        )
                        created_videos.append((video_obj, created))
                
                context = {
                    'videos': created_videos
                }
                return render(request, 'PlaylistMaker/create.html', context)
        
        # マッチしない場合
        context = {'error': 'Invalid YouTube URL'}
        return render(request, 'PlaylistMaker/create.html', context)
    
    # GETリクエストの場合
    return render(request, 'PlaylistMaker/create.html')

def get_playlist_videos(youtube, playlist_id):
    videos = []
    next_page_token = None
    
    while True:
        playlist_response = youtube.playlistItems().list(
            part='snippet',
            playlistId=playlist_id,
            maxResults=50,
            pageToken=next_page_token
        ).execute()
        
        for item in playlist_response['items']:
            video_id = item['snippet']['resourceId']['videoId']
            video = get_video_info(youtube, video_id)
            if video:
                videos.append(video)
        
        next_page_token = playlist_response.get('nextPageToken')
        if not next_page_token:
            break
    
    return videos

def get_video_info(youtube, video_id):
    try:
        video_response = youtube.videos().list(
            part='snippet,statistics',
            id=video_id
        ).execute()
        
        if video_response['items']:
            item = video_response['items'][0]
            snippet = item['snippet']
            statistics = item['statistics']
            
            return {
                'id': video_id,
                'title': snippet['title'],
                'channel': snippet['channelTitle'],
                'image': snippet['thumbnails']['high']['url'],
                'views': int(statistics['viewCount']),
                'published_date': parse_datetime(snippet['publishedAt'])
            }
    except Exception as e:
        print(f"Error fetching video info for {video_id}: {str(e)}")
    
    return None

def video_list(request):
    videos = video_info.objects.all()
    if request.method == 'POST':
        form = VideoSelectionForm(request.POST)
        if form.is_valid():
            for video in videos:
                video.is_selected = request.POST.get(f'video_{video.id}', False) == 'on'
                video.save()
            return redirect('selected_videos')
    return render(request, 'PlaylistMaker/video_list.html', {'videos': videos})

def selected_videos(request):
    selected_videos = video_info.objects.filter(is_selected=True)
    return render(request, 'PlaylistMaker/selected_videos.html', {'videos': selected_videos})

def playlist_detail(request, playlist_id):
    youtube = get_authenticated_service()
    playlist_items = youtube.playlistItems().list(
        part="snippet",
        playlistId=playlist_id,
        maxResults=50
    ).execute()

    videos = []
    for item in playlist_items['items']:
        video_data = {
            'title': item['snippet']['title'],
            'description': item['snippet']['description'],
            'videoId': item['snippet']['resourceId']['videoId']
        }
        videos.append(video_data)

    return render(request, 'PlaylistMaker/playlist_detail.html', {'videos': videos, 'playlist_id': playlist_id})