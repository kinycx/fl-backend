from django.contrib import admin

from .models import Podcast


# Register your models here.
class PodcastAdmin(admin.ModelAdmin):
    list_display = ("title", "description")
    search_fields = ("title", "description")


admin.site.register(Podcast, PodcastAdmin)
