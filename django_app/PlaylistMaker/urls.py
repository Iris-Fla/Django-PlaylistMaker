from django.urls import path
from . import views

urlpatterns = [
  path('', views.index, name='index'),
  path('create', views.create, name='create'),
  path('videos/', views.video_list, name='video_list'),
  path('selected-videos/', views.selected_videos, name='selected_videos'),
  path('create-playlist/', views.create_youtube_playlist, name='create_youtube_playlist'),
]