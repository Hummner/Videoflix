import subprocess
from django.conf import settings
from pathlib import Path
from django.utils.text import slugify



class ConvertVideoToHls():

    def __init__(self, video_path, title):
        # self.title = slugify(title) kesobb!!!!
        self.title = title
        self.video_path = Path(video_path)
        self.video_name = self.video_path.name
        self.video_stem = self.video_path.stem
        self.video_parent = self.video_path.parent
        self.video_suffix = self.video_path.suffix

    def convert_video_480p(self):
        hls_dir = Path(settings.MEDIA_ROOT) / "videos" / self.title / "hls" / "480p"
        hls_dir.mkdir(parents=True, exist_ok=True)

        output_m3u8 = hls_dir / f"{self.video_stem}.m3u8"
        segment_pattern = hls_dir / f"{self.video_stem}%d.ts"




        result = subprocess.run(
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
                    check=True
                )
        
        print(result.stderr)


