from django.shortcuts import render
from .models import video_info

# Create your views here.

def index(request):
  # data = video_info.objects.all()
  # params = {
  #   'title': 'video info',
  #   'message': '動画一覧',
  #   'data': data,
  # }

  return render(request, 'PlaylistMaker/index.html',params)