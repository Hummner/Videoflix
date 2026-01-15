from rest_framework.views import APIView
from .serializers import VideoListSerializer
from rest_framework.response import Response
from ..models import Video
from pathlib import Path
from django.conf import settings
from django.http import HttpResponse


class VideoListViewer(APIView):

    def get(self, request):
        queryset = Video.objects.filter(status="ready")
        serializer = VideoListSerializer(queryset, context={"request": request}, many=True)

        return Response(serializer.data)
    
class VideoViewer(APIView):

    def get(self, request, movie_id, resolution):
        video = Video.objects.get(pk=movie_id)
        content = Path(settings.MEDIA_ROOT) / "videos" / video.title / "hls" / resolution / f"{video.title}.m3u8"

        return HttpResponse(
            content,
            content_type="application/vnd.apple.mpegurl"
        )

