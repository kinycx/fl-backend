import uuid
import boto3
import html

# import tempfile
# import requests
from urllib.parse import quote
from datetime import datetime
from django.db import models
from rest_framework import serializers

from podcast_collection.models import PodcastCollection
from podcaster.models import Podcaster
from django.conf import settings


s3 = boto3.client(
    service_name="s3",
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    region_name="eu-north-1",
)


# Create your models here.
class Podcast(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200, unique=True)
    description = models.TextField(null=True, blank=True, unique=True)
    duration = models.IntegerField(null=True, blank=True)
    audio_file = models.FileField(
        upload_to=settings.AUDIO_UPLOAD_FOLDER, null=True, blank=True, max_length=500
    )
    audio_url = models.URLField(max_length=500, null=True, blank=True)
    cover_file = models.ImageField(
        upload_to=settings.COVER_UPLOAD_FOLDER, null=True, blank=True, max_length=500
    )
    cover_url = models.URLField(max_length=500, null=True, blank=True)
    insert_time = models.DateTimeField(null=True)
    update_time = models.DateTimeField(auto_now=True)
    collection = models.ForeignKey(
        PodcastCollection, on_delete=models.CASCADE, null=True, blank=True
    )
    podcasters = models.ManyToManyField(Podcaster, blank=True)

    def __unicode__(self):
        return self.title

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initial_values = {
            field.name: getattr(self, field.name) for field in self._meta.get_fields()
        }

    def __str__(self):
        return self.title

    @property
    def changed_fields(self):
        return {
            field.name: getattr(self, field.name)
            for field in self._meta.get_fields()
            if getattr(self, field.name) != self.initial_values[field.name]
        }

    # override save method to add audio_url field
    def save(self, *args, **kwargs):
        sf = "/~"  # safe characters, including %
        self.title = html.unescape(self.title)
        self.description = html.unescape(self.description)

        if "audio_file" in self.changed_fields:
            filename = quote(self.audio_file.name.replace(" ", "_"), safe=sf)
            key = f"{settings.AUDIO_UPLOAD_FOLDER}{filename}"
            self.audio_url = (
                f"https://{settings.AWS_S3_BUCKET_NAME}.s3.amazonaws.com/{key}"
            )
        if "cover_file" in self.changed_fields:
            filename = quote(self.cover_file.name.replace(" ", "_"), safe=sf)
            key = f"{settings.COVER_UPLOAD_FOLDER}{filename}"
            self.cover_url = (
                f"https://{settings.AWS_S3_BUCKET_NAME}.s3.amazonaws.com/{key}"
            )

        if self.insert_time is None:
            self.insert_time = datetime.now().time()

        super().save(*args, **kwargs)


class PodcastSerializer(serializers.ModelSerializer):
    class Meta:
        model = Podcast
        fields = "__all__"
