from django.contrib import admin

from .models import PodcastCollection


# Register your models here.
class PodcastCollectionAdmin(admin.ModelAdmin):
    list_display = ("title", "description", "podcasts")
    search_fields = ("title", "description", "podcasts")
    list_filter = ("title", "description", "podcasts")


admin.site.register(PodcastCollection, PodcastCollectionAdmin)
