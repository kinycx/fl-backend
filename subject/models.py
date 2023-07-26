from django.db import models

# Create your models here.
class Subject(models.Model):
    id = models.AutoField(primary_key=True, default=0, unique=True, null=False)
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    
    def __unicode__(self):
        return self.name