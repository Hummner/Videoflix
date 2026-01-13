from django.db.models.signals import post_save
from .models import Video
from django.dispatch import receiver
from .converter.hls_converter import ConvertVideoToHls

@receiver(post_save, sender=Video)
def video_post_save(sender, instance, created, **kwargs):
    print("Video saved")

    if created:
        video_name = instance.video_file.name
        video_title = instance.title
        video = ConvertVideoToHls(video_title, video_name)
        video.convert_video_480p()

        ##was macht geanu pathlib