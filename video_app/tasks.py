import django_rq
from .converter.hls_converter import ConvertVideoToHls
from pathlib import Path
from django.conf import settings
import shutil
from django.utils.text import slugify



def convert_video_all(instance):
        video = ConvertVideoToHls(instance)
        video.get_status()

        queue = django_rq.get_queue("default", autocommit=True)
        job1080 = queue.enqueue(video.convert_video_1080p)
        job720 = queue.enqueue(video.convert_video_720p)
        job480 = queue.enqueue(video.convert_video_480p)
        job_thumbnail = queue.enqueue(video.create_thumbnail_url_path, instance)

        queue.enqueue(video.get_status, depends_on=[job480, job720, job1080, job_thumbnail])


def delete_raw_video(instance):
        pass


def delete_video_dir(instance):
        path = Path(settings.MEDIA_ROOT) / "videos" / f"{instance.pk}"
        shutil.rmtree(path)

        temp_path = Path(settings.MEDIA_ROOT) / "raw" / f"{slugify(instance.title)}"
        shutil.rmtree(temp_path)