import uuid
from django.db import models
from django.contrib.postgres import fields
from rest_framework import serializers

from podcast_collection.models import PodcastCollection
from podcaster.models import Podcaster


# Create your models here.
class Podcast(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    duration = models.DurationField(null=True, blank=True)
    audio_url = models.URLField(null=True, blank=True)
    cover = models.URLField(null=True, blank=True)
    insert_time = models.TimeField(auto_now_add=True)
    update_time = models.TimeField(auto_now=True)
    collection = models.ForeignKey(
        PodcastCollection, on_delete=models.CASCADE, null=True, blank=True
    )
    podcasters = models.ManyToManyField(Podcaster, blank=True)

    def __unicode__(self):
        return self.title


class PodcastSerializer(serializers.ModelSerializer):
    class Meta:
        model = Podcast
        fields = "__all__"
