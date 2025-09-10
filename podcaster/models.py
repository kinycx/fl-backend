# Create your models here.
import uuid

from django.db import models


class Podcaster(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="images/Podcasters", null=True, blank=True)
    presentation = models.TextField(blank=True)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name
