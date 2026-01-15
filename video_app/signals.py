from django.db.models.signals import post_save, post_delete
from .models import Video
from django.dispatch import receiver
from .tasks import convert_video_all, delete_video_dir

@receiver(post_save, sender=Video)
def video_post_save(sender, instance, created, **kwargs):
    print("Video saved")

    if created:
        print("Convert starting...")
        convert_video_all(instance)

@receiver(post_delete, sender=Video)
def video_post_delete(sender, instance, *args, **kwargs):

    delete_video_dir(instance)

        

        