from rest_framework import serializers
from ..models import Video
from pathlib import Path


class VideoListSerializer(serializers.ModelSerializer):

    thumbnail_url = serializers.SerializerMethodField()

    def get_thumbnail_url(self, obj):

        request = self.context['request']
        url = request.build_absolute_uri(obj.thumbnail_url)

        return url

    class Meta:
        model = Video
        fields = ['id', 'created_at', 'category', 'title', 'description', 'thumbnail_url']
        read_only_fields = ['id', 'created_at', 'category', 'title', 'description', 'thumbnail_url']

