
from django.urls import path, include
from .views import VideoViewer


urlpatterns = [
    path('api/video', VideoViewer.as_view(), name="video-viewer"),
]