# signals.py
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.management import call_command
from .models import Podcast


@receiver(post_save, sender=Podcast)
@receiver(post_delete, sender=Podcast)
def update_feed(sender, **kwargs):
    call_command("gen_feed")
