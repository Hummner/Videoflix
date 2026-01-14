import django_rq
from .converter.hls_converter import ConvertVideoToHls



def convert_video_all(instance):
        video = ConvertVideoToHls(instance)
        video.get_status()

        queue = django_rq.get_queue("default", autocommit=True)
        job1080 = queue.enqueue(video.convert_video_1080p)
        job720 = queue.enqueue(video.convert_video_720p)
        job480 = queue.enqueue(video.convert_video_480p)

        queue.enqueue(video.get_status, depends_on=[job480, job720, job1080])

def delete_raw_video(instance):
        pass