from django.db import models

# Create your models here.


class Video(models.Model):
    created_at=models.DateTimeField(auto_now_add=True)
    title=models.CharField(max_length=255)
    description=models.CharField(max_length=500)
    thumbnail_url=models.CharField()
    category=models.CharField(choices="")
