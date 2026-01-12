from rest_framework import serializers
from ..models import Video


class VideoUplaodSerializer(serializers.ModelSerializer):

    class Meta:
        model = Video
        fields = ['id', 'created_at', 'category', 'title', 'description', 'thumbnail_url', 'video_file', 'thumbnail_file']
        read_only_fields = ['created_at', 'thumbnail_url']