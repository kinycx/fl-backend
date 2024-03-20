import os
import boto3
from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Rss201rev2Feed

from podcast.models import Podcast

AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY")
BUCKET_NAME = os.getenv("BUCKET_NAME")

s3 = boto3.client(
    service_name="s3",
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name="eu-north-1",
)

bucket_url = f"https://{BUCKET_NAME}.s3.{s3.meta.region_name}.amazonaws.com/"


class iTunesPodcastsFeedGenerator(Rss201rev2Feed):
    def rss_attributes(self):
        return {
            "version": self._version,
            "xmlns:itunes": "http://www.itunes.com/dtds/podcast-1.0.dtd",
            "xmlns:googleplay": "http://www.google.com/schemas/play-podcasts/1.0",
            "xmlns:atom": "http://www.w3.org/2005/Atom",  # Add this line
        }


class PodcastFeed(Feed):
    feed_type = iTunesPodcastsFeedGenerator
    title = "Podcast Radio Frequenza Libera - On demand"
    link = "https://fl-backend.replit.app/feed/rss/"
    description = "Tutte le registrazioni delle nostre dirette in Podcast!"
    author_name = "Radio Frequenza Libera"
    author_email = "rfl.radiofrequenzalibera@gmail.com"
    categories = ("Arts", "Games & Hobbies > Video Games", "News & Politics")
    image = "https://www.aandmedu.in/wp-content/uploads/2021/11/1-1-Aspect-Ratio-1024x1024.jpg"

    def items(self):
        return Podcast.objects.all().order_by("-insert_time")

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.description

    def item_link(self, item):
        return item.audio_url

    def item_enclosure_url(self, item):
        return item.audio_url

    def item_enclosure_length(self, item):
        key = item.audio_url.split("amazonaws.com/")[-1]
        response = s3.head_object(Bucket=BUCKET_NAME, Key=key)
        return response["ContentLength"]

    def item_enclosure_mime_type(self, item):
        return "audio/mpeg"
