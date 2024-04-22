import uuid
from django.db import models
from django.contrib.postgres import fields
from rest_framework import serializers
from django.conf import settings

from podcast_collection.models import PodcastCollection
from podcaster.models import Podcaster

audio_upload_folder = "MP3_PODCAST/"
cover_upload_folder = "podcast_covers/"

# Create your models here.
class Podcast(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    duration = models.DurationField(null=True, blank=True)
    audio_file = models.FileField(upload_to=audio_upload_folder, null=True, blank=True)
    audio_url = models.URLField(max_length=500, null=True, blank=True)
    cover_file = models.ImageField(upload_to=cover_upload_folder, null=True, blank=True)
    cover_url = models.URLField(null=True, blank=True)
    insert_time = models.TimeField(auto_now_add=True)
    update_time = models.TimeField(auto_now=True)
    collection = models.ForeignKey(
        PodcastCollection, on_delete=models.CASCADE, null=True, blank=True
    )
    podcasters = models.ManyToManyField(Podcaster, blank=True)

    def __unicode__(self):
        return self.title

    # override save method to add audio_url field
    def save(self, *args, **kwargs):
        if self.audio_file:
            self.audio_url = f"https://{settings.AWS_S3_BUCKET_NAME}.s3.eu-north-1.amazonaws.com/{audio_upload_folder}{self.audio_file.name.replace(' ', '_')}"
        if self.cover_file:
            self.cover_url = f"https://{settings.AWS_S3_BUCKET_NAME}.s3.eu-north-1.amazonaws.com/{cover_upload_folder}{self.cover_file.name.replace(' ', '_')}"
        super().save(*args, **kwargs)


class PodcastSerializer(serializers.ModelSerializer):
    class Meta:
        model = Podcast
        fields = "__all__"
