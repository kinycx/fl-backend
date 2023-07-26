from django.db import models



class Podcaster(models.Model):
        id = models.AutoField(primary_key=True, default=0, unique=True, null=False)
        name = models.CharField(max_length=100)
        image = models.ImageField(upload_to='images/Podcasters', null=True, blank=True)
        presentation = models.TextField(null=True, blank=True)
        
    
        def __unicode__(self):
            return self.name