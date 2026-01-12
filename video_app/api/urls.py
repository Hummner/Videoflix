
from django.urls import path, include
from .views import VideoUploadView


urlpatterns = [
    path('api/', VideoUploadView.as_view(), name="video-upload"),
]