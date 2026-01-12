from rest_framework.views import APIView
from .serializers import VideoUplaodSerializer
from rest_framework.response import Response


class VideoUploadView(APIView):


    def post(self, request):
        serializer = VideoUplaodSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({"detail":"Upload started"})