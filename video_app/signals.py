from django.db.models.signals import post_save, post_delete
from .models import Video
from django.dispatch import receiver
from .tasks import convert_video_all, delete_video_dir, create_thumbnail_url_after_save, create_new_thumbnail_video
from django.utils.text import slugify
from django.forms.models import model_to_dict

@receiver(post_save, sender=Video)
def video_post_save(sender, instance, created, **kwargs):
    """
    Post-save handler for Video.

    - On create: enqueue full conversion pipeline (HLS + thumbnail + status updates).
    - On update: ensure thumbnail URL/path is normalized, or generate a new thumbnail
      if none exists.
    """
    print("Video saved")

    if created:
        print("Convert starting...")
        convert_video_all(instance)
    if created == False:
        url_ready = check_url(instance)

        if url_ready == False:
            create_thumbnail_url_after_save(instance)
        elif not instance.thumbnail_file:
            create_new_thumbnail_video(instance)

def check_url(instance):
    """
    Check whether the current thumbnail_file still points to the raw upload location.

    Returns:
        bool:
            False -> thumbnail_file appears to be in the raw upload folder (needs processing/move).
            True  -> thumbnail_file does not match the raw upload naming pattern.
    """
    raw_url = f"raw/{slugify(instance.title)}/{slugify(instance.title)}_thumbnail"

    if raw_url in instance.thumbnail_file.name:
        return False
    return True

@receiver(post_delete, sender=Video)
def video_post_delete(sender, instance, *args, **kwargs):
    """
    Post-delete handler for Video.

    Removes the processed video directory and the temporary/raw upload directory.
    """
    delete_video_dir(instance)
