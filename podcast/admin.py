from django.contrib import admin

from .models.podcast import Podcast
from .models.podcast_collection import PodcastCollection
from .models.podcaster import Podcaster

# Register your models here.
admin.site.register(Podcast)
admin.site.register(PodcastCollection)
admin.site.register(Podcaster)