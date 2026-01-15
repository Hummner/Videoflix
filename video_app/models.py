from django.db import models
import os
from django.utils.text import slugify

# Create your models here.



def video_upload_root(instance, filename):
    ext = os.path.splitext(filename)[1]
    title = slugify(instance.title)
    return f"raw/{title}/{title}_raw_video{ext}"

def video_thumbnail_root(instance, filename):
    ext = os.path.splitext(filename)[1]
    title = slugify(instance.title)
    return f"raw/{title}/{title}_thumbnail{ext}"

CATEGORY_CHOICES = [
    ("drama", "Drama"),
    ("crime", "Crime"),
    ("thriller", "Thriller"),
    ("action", "Action"),
    ("comedy", "Comedy"),
    ("romance", "Romance"),
    ("horror", "Horror"),
    ("sci_fi", "Science Fiction (Sci-Fi)"),
    ("fantasy", "Fantasy"),
    ("mystery", "Mystery"),
    ("adventure", "Adventure"),
    ("animation", "Animation"),
    ("documentary", "Documentary"),
    ("family", "Family"),
    ("war", "War"),
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
    thumbnail_file=models.ImageField(upload_to=video_thumbnail_root, blank=True, editable=False)
    category=models.CharField(choices=CATEGORY_CHOICES)
    video_file = models.FileField(upload_to=video_upload_root, editable=False)
    status = models.CharField(choices=STATUS, default="pending")
