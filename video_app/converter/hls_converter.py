import subprocess
from django.conf import settings
from pathlib import Path
from django.utils.text import slugify
from video_app.models import Video
import shutil


class ConvertVideoToHls():

    def __init__(self, instance):
        self.title = slugify(instance.title)
        self.video_path = Path(instance.video_file.path)
        self.video_stem = self.video_path.stem
        self.id = instance.pk
        self.hls_dir = Path(settings.MEDIA_ROOT) / "videos" / f"{self.id}" / "hls"


    def get_status(self):
        video = Video.objects.get(pk=self.id)

        if video.status == "processing":
            video.status = "ready"
            print(f"The \"{video.title}\" is ready")
            return video.save(update_fields=['status'])
        
        video.status = "processing"
        return video.save(update_fields=['status'])
    
    def create_thumbnail_url_path(self, instance):
        if not instance.thumbnail_file:
            return self.create_thumbnail(instance)
        
        return self.make_thumbnail_copy(instance)
        
        

    def make_thumbnail_copy(self, instance):
        dest_dir = Path(settings.MEDIA_ROOT) / "videos" / f"{self.id}"
        dest_dir.mkdir(parents=True, exist_ok=True)
        new_path = Path(dest_dir) / f"{self.id}_thumbnail.jpg"

        if Path(instance.thumbnail_file.path).exists():

            shutil.move(
                instance.thumbnail_file.path,
                new_path
            )

        return self.create_thumbnail_url(new_path)

    def create_thumbnail_url(self, path):
        rel_path = path.relative_to(Path(settings.MEDIA_ROOT))
        new_url = Path("/media") / rel_path
        return Video.objects.filter(pk=self.id).update(thumbnail_file=rel_path, thumbnail_url=str(new_url))
    

    def create_thumbnail(self, instance):
        dest_dir = Path(settings.MEDIA_ROOT) / "videos" / f"{self.id}"
        dest_dir.mkdir(parents=True, exist_ok=True)
        output_path = Path(dest_dir) / f"{self.id}_thumbnail.jpg"
        input_path = Path(instance.video_file.path)

        subprocess.run(
            [
            "ffmpeg",
            "-y",
            "-ss", "00:00:02",
            "-i", str(input_path),
            "-vframes", "1",
            "-vf", "scale=800:-2",
            "-q:v", "2",
            str(output_path),
            ]
        )
        print(output_path)

        return self.create_thumbnail_url(output_path)
        
        

    def convert_video_480p(self):
        hls_dir = Path(self.hls_dir) / "480p"
        hls_dir.mkdir(parents=True, exist_ok=True)

        output_m3u8 = hls_dir / "index.m3u8"
        segment_pattern = hls_dir / f"{self.id}_segment_%d.ts"

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
        hls_dir = Path(self.hls_dir) / "720p"
        hls_dir.mkdir(parents=True, exist_ok=True)

        output_m3u8 = hls_dir / "index.m3u8"
        segment_pattern = hls_dir / f"{self.id}_segment_%d.ts"

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
        hls_dir = Path(self.hls_dir) / "1080p"
        hls_dir.mkdir(parents=True, exist_ok=True)

        output_m3u8 = hls_dir / "index.m3u8"
        segment_pattern = hls_dir / f"{self.id}_segment_%d.ts"

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


