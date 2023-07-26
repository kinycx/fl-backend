from django.db import models

# Create your models here.
# Create your models here.
class Collection(models.Model):
        id = models.AutoField(primary_key=True, default=0, unique=True, null=False)
        name = models.CharField(max_length=100)
        description = models.TextField(null=True, blank=True)
        insert_time = models.TimeField(auto_now_add=True)
        update_time = models.TimeField(auto_now=True)
        cover = models.ImageField(upload_to='images/Collection', null=True, blank=True)

        def __unicode__(self):
            return self.name