from django.apps import AppConfig


class VideoAppConfig(AppConfig):
    name = 'video_app'
    verbose_name = 'Video Management'

    def ready(self):
        from . import signals
