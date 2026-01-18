import django_rq
from .converter.hls_converter import ConvertVideoToHls
from pathlib import Path
from django.conf import settings
import shutil
from django.utils.text import slugify



def convert_video_all(instance):
        """
        Enqueue all conversion jobs for a Video instance (HLS renditions + thumbnail).

        Workflow:
        1) Instantiate the converter and set status to "processing".
        2) Enqueue HLS conversions (1080p/720p/480p) and thumbnail handling.
        3) Enqueue a final status toggle back to "ready" once all jobs are finished.

        Args:
            instance (Video): The Video object to process.
        """
        video = ConvertVideoToHls(instance)
        video.get_status()

        queue = django_rq.get_queue("default", autocommit=True)
        job1080 = queue.enqueue(video.convert_video_1080p)
        job720 = queue.enqueue(video.convert_video_720p)
        job480 = queue.enqueue(video.convert_video_480p)
        job_thumbnail = queue.enqueue(video.create_thumbnail_url_path, instance)

        queue.enqueue(video.get_status, depends_on=[job480, job720, job1080, job_thumbnail])


def delete_raw_video(instance):
        """
        Placeholder for deleting the original/raw uploaded video file if needed.

        Args:
            instance (Video): The Video object whose raw file should be removed.
        """
        pass


def delete_video_dir(instance):
        """
        Remove the processed video directory and the temporary/raw upload directory.

        WARNING:
        - This permanently deletes files from disk.
        - Works only with local filesystem storage.

        Args:
            instance (Video): The Video object whose folders should be removed.
        """
        path = Path(settings.MEDIA_ROOT) / "videos" / f"{instance.pk}"
        shutil.rmtree(path)

        temp_path = Path(settings.MEDIA_ROOT) / "raw" / f"{slugify(instance.title)}"
        shutil.rmtree(temp_path)

def create_thumbnail_url_after_save(instance):
        """
        Enqueue thumbnail relocation/generation after a model save (update case).

        Args:
            instance (Video): The Video object to process.
        """
        video = ConvertVideoToHls(instance)
        queue = django_rq.get_queue("default", autocommit=True)
        queue.enqueue(video.create_thumbnail_url_path, instance)



def create_new_thumbnail_video(instance):
        """
        Generate a new thumbnail image after the previously selected one was removed.

        Args:
            instance (Video): The Video object for which the thumbnail should be generated.
        """
        video = ConvertVideoToHls(instance)
        print(video)
        queue = django_rq.get_queue("default", autocommit=True)
        queue.enqueue(video.create_thumbnail, instance)
