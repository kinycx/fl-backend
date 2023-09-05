from django.db import models
from django.contrib.postgres import fields
from rest_framework import serializers

from .podcast_collection import PodcastCollection
from .podcaster import Podcaster

# Create your models here.
class Podcast(models.Model):
        id = models.AutoField(primary_key=True, default=0, unique=True, null=False)
        name = models.CharField(max_length=100)
        description = models.TextField(null=True, blank=True)
        duration = models.DurationField(null=True, blank=True)
        cover = models.ImageField(upload_to='images/Podcast', null=True, blank=True)
        insert_time = models.TimeField(auto_now_add=True)
        update_time = models.TimeField(auto_now=True)
        collection = models.ForeignKey(PodcastCollection, on_delete=models.CASCADE, null=True, blank=True)
        podcasters = models.ManyToManyField(Podcaster, blank=True)
        
        def __unicode__(self):
            return self.name
        
class PodcastSerializer(serializers.ModelSerializer):
    class Meta:
        model = Podcast
        fields = '__all__'


