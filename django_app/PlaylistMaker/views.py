import re
from googleapiclient.discovery import build
from django.shortcuts import render
from django.conf import settings
from .models import video_info
from django.utils.dateparse import parse_datetime

# Create your views here.

def index(request):
  data = video_info.objects.all()
  params = {
    'videos': data,
  }

  return render(request, 'PlaylistMaker/index.html',params)

def create(request):
    if request.method == 'POST':
        url = request.POST.get('url')
        youtube = build('youtube', 'v3', developerKey=settings.YOUTUBE_API_KEY)
        
        patterns = [
            r'(?:https?:\/\/)?(?:www\.)?youtube\.com\/watch\?v=([^&]+)',
            r'(?:https?:\/\/)?(?:www\.)?youtu\.be\/([^?]+)',
            r'(?:https?:\/\/)?(?:www\.)?youtube\.com\/embed\/([^?]+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                video_id = match.group(1)
                videos_response = youtube.videos().list(
                    part='snippet,statistics',
                    id=video_id
                ).execute()
                
                if videos_response['items']:
                    item = videos_response['items'][0]
                    snippet = item['snippet']
                    statistics = item['statistics']
                    
                    # Create or update video_info object
                    video, created = video_info.objects.update_or_create(
                        videoid=video_id,
                        defaults={
                            'title': snippet['title'],
                            'channel': snippet['channelTitle'],
                            'image': snippet['thumbnails']['high']['url'],
                            'url': f"https://www.youtube.com/watch?v={video_id}",
                            'views': int(statistics['viewCount']),
                            'published_date': parse_datetime(snippet['publishedAt'])
                        }
                    )
                    
                    context = {
                        'video': video,
                        'created': created
                    }
                    return render(request, 'PlaylistMaker/create.html', context)
        
        # If no match found
        context = {'error': 'Invalid YouTube URL'}
        return render(request, 'PlaylistMaker/create.html', context)
    
    # If GET request
    return render(request, 'PlaylistMaker/create.html')