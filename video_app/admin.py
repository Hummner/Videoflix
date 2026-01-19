from django.contrib import admin
from .models import Video

# Register your models here.

admin.site.site_header = 'Videoflix Admin Panel'
admin.site.site_title = 'Admin | Videoflix'


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Video model.

    - Makes `video_file` read-only after the object is created.
    - Hides internal fields from the admin form.
    """

    def get_readonly_fields(self, request, obj=None):
        """Allow editing `video_file` only on creation, not on update."""
        if obj:
            return ("video_file",)
        return super().get_readonly_fields(request, obj)

    # Fields not shown in the admin form
    exclude = ("thumbnail_url", "status")
    



