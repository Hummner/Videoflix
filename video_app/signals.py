from django.db.models.signals import post_save
from .models import Video
from django.dispatch import receiver

@receiver(post_save, sender=Video)
def video_post_save(sender, instance, created, **kwargs):
    print("Video saved")
    if created:
        print('New video created')