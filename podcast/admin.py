from django.contrib import admin

from .models import Podcast


# Register your models here.
class PodcastAdmin(admin.ModelAdmin):
    list_display = ("title", "description", "audio_url", "collection", "podcasters")
    search_fields = ("title", "description", "audio_url", "collection", "podcasters")
    list_filter = ("title", "description", "audio_url", "collection", "podcasters")


admin.site.register(Podcast, PodcastAdmin)
