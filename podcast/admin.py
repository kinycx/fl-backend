from django.contrib import admin

from .models import Podcast


# Register your models here.
class PodcastAdmin(admin.ModelAdmin):
    list_display = ("title", "description", "insert_time")
    search_fields = ("title", "description", "insert_time")


admin.site.register(Podcast, PodcastAdmin)
