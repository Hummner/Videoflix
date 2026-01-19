from rest_framework.views import APIView
from .serializers import VideoListSerializer, VideoViewerSerializer
from rest_framework.response import Response
from ..models import Video
from pathlib import Path
from django.conf import settings
from django.http import FileResponse
from auth_app.api.authentication import CookieJWTAuthentication
from rest_framework.permissions import IsAuthenticated


class VideoListViewer(APIView):
    """
    List endpoint for all videos that are ready to be viewed.

    Authentication:
    - Uses JWTAuthentication (CookieJWTAuthentication).
    
    Permissions:
    - User must be authenticated
    - Only active users are allowed to access this endpoint
    """
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]
    

    def get(self, request):
        """
        Return a list of "ready" videos.

        The serializer builds an absolute `thumbnail_url` using the request context.
        """
        queryset = Video.objects.filter(status="ready")
        serializer = VideoListSerializer(queryset, context={"request": request}, many=True)

        return Response(serializer.data)
    
class VideoViewer(APIView):
    """
    Serves the HLS playlist (index.m3u8) for a specific video and resolution.

    Authentication:
    - Uses JWTAuthentication (SimpleJWT).

    Permissions:
    - User must be authenticated
    - Only active users are allowed to access this endpoint

    Validation:
    - Uses VideoViewerSerializer to validate the video id and allowed resolutions.
    """
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, movie_id, resolution):
        """
        Return the HLS master playlist for a given video id and resolution.

        Args:
            movie_id (int/str): Video identifier from the URL.
            resolution (str): Requested resolution ("480p", "720p", "1080p").
        """
        serializer = VideoViewerSerializer(data={"resolution": resolution, "id": movie_id})
        serializer.is_valid(raise_exception=True)
        id = serializer.validated_data["id"]
        resolution = serializer.validated_data["resolution"]

        content = Path(settings.MEDIA_ROOT) / "videos" / f"{id.pk}" / "hls" / resolution / "index.m3u8"
        return FileResponse(
            open(content, "rb"),
            content_type="application/vnd.apple.mpegurl"
        )
    
class VideoSegmentViewer(APIView):
    """
    Serves individual HLS segment files (*.ts) for a video.

    Authentication:
    - Uses JWTAuthentication (SimpleJWT).

    Permissions:
    - User must be authenticated
    - Only active users are allowed to access this endpoint
    """
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]


    def get(self, request, movie_id, resolution, segment):
        """
        Return a specific HLS segment file.

        Args:
            movie_id (int/str): Video identifier from the URL.
            resolution (str): Requested resolution folder name.
            segment (str): Segment filename (e.g. "44_segment_0.ts").
        """
        content = Path(settings.MEDIA_ROOT) / "videos" / f"{movie_id}" / "hls" / resolution / segment
        return FileResponse(
            open(content, "rb"),
            content_type="video/MP2T"
        )
