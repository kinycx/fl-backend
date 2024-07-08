from django.contrib import admin

from .models import PodcastCollection


# Register your models here.
class PodcastCollectionAdmin(admin.ModelAdmin):
    list_display = ("title", "description")
    search_fields = ("title", "description")


admin.site.register(PodcastCollection, PodcastCollectionAdmin)
