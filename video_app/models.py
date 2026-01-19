from django.db import models
import os
from django.utils.text import slugify

# Create your models here.



def video_upload_root(instance, filename):
    """Return the upload path for the raw video file."""
    ext = os.path.splitext(filename)[1]
    title = slugify(instance.title)
    return f"raw/{title}/{title}_raw_video{ext}"

def video_thumbnail_root(instance, filename):
    """Return the upload path for the raw thumbnail file."""
    ext = os.path.splitext(filename)[1]
    title = slugify(instance.title)
    return f"raw/{title}/{title}_thumbnail{ext}"

CATEGORY_CHOICES = [
    ("drama", "Drama"),
    ("crime", "Krimi"),
    ("thriller", "Thriller"),
    ("action", "Action"),
    ("comedy", "Komödie"),
    ("romance", "Romantik"),
    ("horror", "Horror"),
    ("sci_fi", "Science-Fiction"),
    ("fantasy", "Fantasy"),
    ("mystery", "Mystery"),
    ("adventure", "Abenteuer"),
    ("animation", "Animation"),
    ("documentary", "Dokumentarfilm"),
    ("family", "Familie"),
    ("war", "Krieg"),
    ("western", "Western"),
    ("musical", "Musical"),
]


STATUS = (
        ("pending", "Pending"),
        ("processing", "Processing"),
        ("ready", "Ready")
    )



class Video(models.Model):
    created_at=models.DateTimeField(auto_now_add=True)
    title=models.CharField(max_length=255)
    description=models.CharField(max_length=500)
    thumbnail_url=models.CharField(blank=True)
    thumbnail_file=models.ImageField(upload_to=video_thumbnail_root, blank=True, help_text="" \
    "If no thumbnail is provided, one will be generated automatically. You can add a custom one later.")
    category=models.CharField(choices=CATEGORY_CHOICES)
    video_file = models.FileField(upload_to=video_upload_root, help_text="The video file itself cannot be modified after it has been uploaded.")
    status = models.CharField(choices=STATUS, default="pending")
