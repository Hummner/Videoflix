from rest_framework import serializers
from ..models import Video


class VideoListSerializer(serializers.ModelSerializer):
    """
    Serializer used for listing videos.

    - Returns basic video metadata.
    - Exposes `thumbnail_url` as an absolute URL so it can be used directly
      by the frontend.
    """

    thumbnail_url = serializers.SerializerMethodField()

    def get_thumbnail_url(self, obj):
        """
        Build a fully qualified (absolute) URL for the thumbnail.

        This uses the current request context to include scheme and host
        (e.g. https://example.com/media/...).
        """
        request = self.context['request']
        return request.build_absolute_uri(obj.thumbnail_url)

    class Meta:
        model = Video
        fields = [
            'id',
            'created_at',
            'category',
            'title',
            'description',
            'thumbnail_url',
        ]
        read_only_fields = fields


class VideoViewerSerializer(serializers.Serializer):
    """
    Serializer used when a client requests to view/play a video.

    Validates:
    - The video ID exists.
    - The requested resolution is supported by the system.
    """

    id = serializers.PrimaryKeyRelatedField(
        queryset=Video.objects.all(),
        error_messages={
            "does_not_exist": "Video not found.",
            "incorrect_type": "Invalid video identifier.",
        }
    )

    resolution = serializers.CharField()

    def validate_resolution(self, value):
        """
        Ensure the requested resolution is supported.

        Allowed values:
        - 480p
        - 720p
        - 1080p
        """
        allowed_values = ["480p", "720p", "1080p"]
        if value not in allowed_values:
            raise serializers.ValidationError({"error": "Invalid resolution"})
        return value
