import re
from googleapiclient.discovery import build
from django.shortcuts import render,redirect
from django.conf import settings
from .models import video_info
from django.utils.dateparse import parse_datetime
from .forms import VideoSelectionForm

# Create your views here.

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

#   params = {
#     'videos': videos,
#   }

  return render(request, 'PlaylistMaker/index.html', {'videos': videos})

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