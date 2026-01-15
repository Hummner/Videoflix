from rest_framework.views import APIView
from .serializers import VideoListSerializer, VideoViewerSerializer
from rest_framework.response import Response
from ..models import Video
from pathlib import Path
from django.conf import settings
from django.http import HttpResponse, FileResponse
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated


class VideoListViewer(APIView):
    authentication_classes = [JWTAuthentication]
    

    def get(self, request):
        queryset = Video.objects.filter(status="ready")
        serializer = VideoListSerializer(queryset, context={"request": request}, many=True)

        return Response(serializer.data)
    
class VideoViewer(APIView):
    authentication_classes = [JWTAuthentication]

    def get(self, request, movie_id, resolution):
        serializer = VideoViewerSerializer(data={"resolution": resolution, "id": movie_id})
        serializer.is_valid(raise_exception=True)
        id = serializer.validated_data["id"]
        resolution = serializer.validated_data["resolution"]


        content = Path(settings.MEDIA_ROOT) / "videos" / f"{id.pk}" / "hls" / resolution / "index.m3u8"
        url = request.build_absolute_uri(content)

    
        return FileResponse(
            open(content, "rb"),
            content_type="application/vnd.apple.mpegurl"
        )
    
class VideoSegmentViewer(APIView):
    authentication_classes = [JWTAuthentication]


    def get(self, request, movie_id, resolution, segment):
        content = Path(settings.MEDIA_ROOT) / "videos" / f"{movie_id}" / "hls" / resolution / segment
        url = request.build_absolute_uri(content)
        return FileResponse(
            open(content, "rb"),
            content_type="video/MP2T"
        )

