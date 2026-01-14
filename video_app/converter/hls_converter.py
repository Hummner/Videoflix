import subprocess
from django.conf import settings
from pathlib import Path
from django.utils.text import slugify
from video_app.models import Video


class ConvertVideoToHls():

    def __init__(self, instance):
        self.title = slugify(instance.title)
        self.video_path = Path(instance.video_file.path)
        self.video_stem = self.video_path.stem
        self.pk = instance.pk


    def get_status(self):
        video = Video.objects.get(pk=self.pk)

        if video.status == "processing":
            video.status = "ready"
            print(f"The \"{video.title}\" is ready")
            return video.save(update_fields=['status'])
        
        video.status = "processing"
        return video.save(update_fields=['status'])
        

    def convert_video_480p(self):
        hls_dir = Path(settings.MEDIA_ROOT) / "videos" / self.title / "hls" / "480p"
        hls_dir.mkdir(parents=True, exist_ok=True)

        output_m3u8 = hls_dir / f"{self.video_stem}.m3u8"
        segment_pattern = hls_dir / f"{self.video_stem}%d.ts"




        subprocess.run(
                    [
                        "ffmpeg",
                        "-y",
                        "-i", str(self.video_path),
                        "-vf", "scale=-2:480",
                        "-c:v", "libx264",
                        "-crf", "23",
                        "-preset", "fast",
                        "-c:a", "aac",
                        "-hls_time", "10",
                        "-hls_list_size", "0",
                        "-start_number", "0",
                        "-hls_segment_filename", str(segment_pattern),
                        "-f", "hls",
                        str(output_m3u8),
                    ],
                    capture_output=True
                )
        

    def convert_video_720p(self):
        hls_dir = Path(settings.MEDIA_ROOT) / "videos" / self.title / "hls" / "720p"
        hls_dir.mkdir(parents=True, exist_ok=True)

        output_m3u8 = hls_dir / f"{self.video_stem}.m3u8"
        segment_pattern = hls_dir / f"{self.video_stem}%d.ts"

        subprocess.run(
                    [
                        "ffmpeg",
                        "-y",
                        "-i", str(self.video_path),
                        "-vf", "scale=-2:720",
                        "-c:v", "libx264",
                        "-crf", "23",
                        "-preset", "fast",
                        "-c:a", "aac",
                        "-hls_time", "10",
                        "-hls_list_size", "0",
                        "-start_number", "0",
                        "-hls_segment_filename", str(segment_pattern),
                        "-f", "hls",
                        str(output_m3u8),
                    ],
                    capture_output=True
                )
        
    def convert_video_1080p(self):
        hls_dir = Path(settings.MEDIA_ROOT) / "videos" / self.title / "hls" / "1080p"
        hls_dir.mkdir(parents=True, exist_ok=True)

        output_m3u8 = hls_dir / f"{self.video_stem}.m3u8"
        segment_pattern = hls_dir / f"{self.video_stem}%d.ts"

        subprocess.run(
                    [
                        "ffmpeg",
                        "-y",
                        "-i", str(self.video_path),
                        "-vf", "scale=-2:1080",
                        "-c:v", "libx264",
                        "-crf", "23",
                        "-preset", "fast",
                        "-c:a", "aac",
                        "-hls_time", "10",
                        "-hls_list_size", "0",
                        "-start_number", "0",
                        "-hls_segment_filename", str(segment_pattern),
                        "-f", "hls",
                        str(output_m3u8),
                    ],
                    capture_output=True
                )


