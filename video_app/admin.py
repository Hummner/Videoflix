from django.contrib import admin
from .models import Video

# Register your models here.


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):

    def get_readonly_fields(self, request, obj = ...):

        if obj:
            return ("video_file",)

        return super().get_readonly_fields(request, obj)
    exclude = ("thumbnail_url", "status")