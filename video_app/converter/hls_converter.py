import subprocess
from django.conf import settings
from pathlib import Path



class ConvertVideoToHls():

    def __init__(self, video_titel, video_name):
        self.video_titel = video_titel
        self.video_name = video_name

    def convert_video_480p(self):
        media_root = Path(settings.MEDIA_ROOT)

        input_video = media_root / "video" / self.video_titel / self.video_name

        hls_dir = media_root / "video" / self.video_titel / "HLS"
        hls_dir.mkdir(parents=True, exist_ok=True)

        output_m3u8 = hls_dir / f"{Path(self.video_name).stem}.m3u8"
        segment_pattern = hls_dir / f"{Path(self.video_name).stem}%d.ts"


        result = subprocess.run(
                    [
                        "ffmpeg",
                        "-y",
                        "-i", str(input_video),
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


