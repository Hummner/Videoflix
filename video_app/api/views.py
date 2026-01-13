from rest_framework.views import APIView
from .serializers import VideoSerializer
from rest_framework.response import Response


class VideoViewer(APIView):

    def get(self, request):
        pass