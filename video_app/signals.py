from django.db.models.signals import post_save
from .models import Video
from django.dispatch import receiver
from .converter.hls_converter import ConvertVideoToHls
from pathlib import Path

@receiver(post_save, sender=Video)
def video_post_save(sender, instance, created, **kwargs):
    print("Video saved")
    print("name: ", instance.video_file.name)
    print("name: ", instance.video_file.path)

    if created:
        print("Convert staring...")
        video = ConvertVideoToHls(instance.video_file.path, instance.title)
        video.convert_video_480p()

        ##was macht geanu pathlib