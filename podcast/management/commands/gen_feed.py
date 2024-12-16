from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
import logging
import xml.etree.ElementTree as ET
from services.feed import iTunesPodcastsFeedGenerator, email, PODCAST_LIMIT
from podcast.models import Podcast

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = "Generate RSS feed and save to S3"

    def handle(self, *args, **options):
        # Generate the feed using iTunesPodcastsFeedGenerator
        feed = iTunesPodcastsFeedGenerator(
            title="Podcast Radio Frequenza Libera",
            link="https://www.frequenzalibera.it",
            description="Dal 2013 frequenza Libera vive e da voce agli studenti e alle studentesse degli atenei senza distinzione, "
            "associazione web radio fondata dagli stessi in modalità volontaria.Patrocinata dal Politecnico di Bari, è tutt'ora "
            "uno spazio di incontro, collaborazione, contaminazione e diffusione. Dai podcast intrattenitivi o divulgativi alle "
            "chiacchierate e interviste con ospiti tra i più svariati, dagli artisti, registi, professori e tanto altro... Seguici, e vedi che ti ascolti!",
            author_name="Radio Frequenza Libera",
            author_email=email,
            categories=("Arts", "Games & Hobbies > Video Games", "News & Politics"),
            image="https://podcast-fl.s3.eu-north-1.amazonaws.com/podcast_media_generics/foto+profilo.jpg",
            language="it",
        )

        podcasts = Podcast.objects.all().order_by("-insert_time")[:PODCAST_LIMIT]

        logger.debug(f"Podcasts: {podcasts.count()}")

        for podcast in podcasts:
            feed.add_item(
                title=podcast.title,
                link=podcast.audio_url,
                description=podcast.description,
                unique_id=podcast.audio_url,
                enclosure_url=podcast.audio_url,
                enclosure_length=podcast.duration,
                enclosure_mime_type="audio/mpeg",
                pubdate=podcast.insert_time,
                enclosure_cover=podcast.cover_url,
            )

        # Convert the feed to a string
        feed_content = feed.writeString("utf-8")

        # Log the response content length and a snippet of the content
        logger.debug(f"Feed content length: {len(feed_content)}")
        # logger.debug(f"Feed content snippet: {feed_content[:100]}")

        # Check if the feed content is empty
        if not feed_content:
            self.stdout.write(self.style.ERROR("The feed content is empty"))
            return

        # Check if the feed content is valid XML
        try:
            ET.fromstring(feed_content)
        except ET.ParseError as e:
            self.stdout.write(self.style.ERROR(f"Invalid XML content: {e}"))
            return

        # Delete the existing feed file if it exists
        file_name = "feed.xml"
        if default_storage.exists(file_name):
            default_storage.delete(file_name)

        # Save the new feed to a file
        file_content = ContentFile(feed_content)
        default_storage.save(file_name, file_content)

        self.stdout.write(self.style.SUCCESS("Successfully saved feed to S3"))
