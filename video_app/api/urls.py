
from django.urls import path, include
from .views import VideoListViewer, VideoViewer


urlpatterns = [
    path('video/', VideoListViewer.as_view(), name="video-list-viewer"),
    path('video/<int:movie_id>/<str:resolution>/index.m3u8', VideoViewer.as_view(), name="video-viewer")
]