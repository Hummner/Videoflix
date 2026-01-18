import subprocess
from django.conf import settings
from pathlib import Path
from django.utils.text import slugify
from video_app.models import Video
import shutil


class ConvertVideoToHls():
    """
    Utility/service class responsible for:
    - Converting an uploaded video into HLS renditions (480p/720p/1080p).
    - Creating or relocating a thumbnail image into a standardized MEDIA_ROOT location.
    - Updating Video model fields (status, thumbnail_file, thumbnail_url) accordingly.

    Notes:
    - This class expects local filesystem storage because it relies on `.path` and direct file operations.
    - Video database updates are mostly done via `QuerySet.update()` to avoid triggering model signals.
    """

    def __init__(self, instance):
        """
        Initialize converter state for a given Video instance.

        Args:
            instance (Video): The Video model instance to process.
        """
        self.title = slugify(instance.title)
        self.video_path = Path(instance.video_file.path)
        self.video_stem = self.video_path.stem
        self.id = instance.pk
        self.hls_dir = Path(settings.MEDIA_ROOT) / "videos" / f"{self.id}" / "hls"


    def get_status(self):
        """
        Toggle video processing status.

        - If current status is "processing", set it to "ready".
        - Otherwise set it to "processing".

        Returns:
            Any: Return value of `video.save(...)`.
        """
        video = Video.objects.get(pk=self.id)

        if video.status == "processing":
            video.status = "ready"
            print(f"The \"{video.title}\" is ready")
            return video.save(update_fields=['status'])
        
        video.status = "processing"
        return video.save(update_fields=['status'])
    
    def create_thumbnail_url_path(self, instance):
        """
        Ensure a thumbnail exists in the target folder and update its URL fields.

        - If no thumbnail_file is attached, generate one from the video.
        - Otherwise, move the existing thumbnail into the standardized destination.

        Args:
            instance (Video): The Video instance (used for current file paths).

        Returns:
            Any: Result of thumbnail URL update operation.
        """
        if not instance.thumbnail_file:
            return self.create_thumbnail(instance)
        
        return self.make_thumbnail_copy(instance)
        
        

    def make_thumbnail_copy(self, instance):
        """
        Move an already uploaded thumbnail file into the standardized destination path.

        Destination:
            MEDIA_ROOT/videos/<id>/<id>_thumbnail.jpg

        Args:
            instance (Video): The Video instance whose `thumbnail_file` is moved.

        Returns:
            Any: Result of updating `thumbnail_file` and `thumbnail_url` in the DB.
        """
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
        """
        Compute relative media path and URL for a thumbnail and persist to the DB.

        Args:
            path (Path): Absolute path to the thumbnail file inside MEDIA_ROOT.

        Returns:
            int: Number of updated rows from `QuerySet.update()`.
        """
        rel_path = path.relative_to(Path(settings.MEDIA_ROOT))
        new_url = Path("/media") / rel_path
        return Video.objects.filter(pk=self.id).update(thumbnail_file=rel_path, thumbnail_url=str(new_url))
    

    def create_thumbnail(self, instance):
        """
        Generate a thumbnail image from the video using ffmpeg.

        - Seeks to 2 seconds.
        - Extracts 1 frame.
        - Scales to width 800px (keeping aspect ratio).
        - Writes to: MEDIA_ROOT/videos/<id>/<id>_thumbnail.jpg

        Args:
            instance (Video): The Video instance providing the source video file.

        Returns:
            Any: Result of updating `thumbnail_file` and `thumbnail_url` in the DB.
        """
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
        """
        Convert the source video to an HLS 480p rendition.

        Output:
            MEDIA_ROOT/videos/<id>/hls/480p/index.m3u8
            MEDIA_ROOT/videos/<id>/hls/480p/<id>_segment_%d.ts
        """
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
        """
        Convert the source video to an HLS 720p rendition.

        Output:
            MEDIA_ROOT/videos/<id>/hls/720p/index.m3u8
            MEDIA_ROOT/videos/<id>/hls/720p/<id>_segment_%d.ts
        """
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
        """
        Convert the source video to an HLS 1080p rendition.

        Output:
            MEDIA_ROOT/videos/<id>/hls/1080p/index.m3u8
            MEDIA_ROOT/videos/<id>/hls/1080p/<id>_segment_%d.ts
        """
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
