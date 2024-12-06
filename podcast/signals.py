import os
import logging
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.management import call_command

from .models import Podcast

# Set up logging
logger = logging.getLogger(__name__)

@receiver(post_save, sender=Podcast)
@receiver(post_delete, sender=Podcast)
def update_feed(sender, **kwargs):
    debug_value = os.getenv("DEBUG")
    logger.info(f"DEBUG value is: {debug_value}")

    if not bool(debug_value):
        logger.info("Generating feed...")
        call_command("gen_feed")
