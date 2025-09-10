import uuid

from django.db import models
from rest_framework import serializers


class PodcastCollection(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    insert_time = models.TimeField(auto_now_add=True)
    update_time = models.TimeField(auto_now=True)
    cover = models.ImageField(upload_to="images/Collection", null=True, blank=True)

    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.title


class PodcastCollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PodcastCollection
        fields = "__all__"
