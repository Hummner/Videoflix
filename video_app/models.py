from django.db import models
import os
import re

# Create your models here.


def video_uplaod_root(instance, filename):
    ext = os.path.splitext(filename)[1]  # z. B. .mp4
    id = instance.id
    title = instance.title.replace(" ", "-")
    return f"videos/{id}/{title}{ext}"

def video_thumbnail_root(instance, filename):
    ext = os.path.splitext(filename)[1]  # z. B. .mp4
    id = instance.id
    title = instance.title.replace(" ", "-")
    return f"videos/{id}/{title}_thumbnail{ext}"

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


class Video(models.Model):
    created_at=models.DateTimeField(auto_now_add=True)
    title=models.CharField(max_length=255)
    description=models.CharField(max_length=500)
    thumbnail_url=models.CharField(blank=True)
    thumbnail_file=models.FileField(upload_to=video_thumbnail_root)
    category=models.CharField(choices=CATEGORY_CHOICES)
    video_file = models.FileField(upload_to=video_uplaod_root)
