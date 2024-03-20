import os
import boto3
import datetime
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
            "xmlns:atom": "http://www.w3.org/2005/Atom",
        }

    def add_root_elements(self, handler):
        super().add_root_elements(handler)
        handler.addQuickElement("itunes:author", "Radio Frequenza Libera")
        handler.addQuickElement("itunes:explicit", "no")
        handler.startElement(
            "itunes:image",
            {
                "href": "https://www.aandmedu.in/wp-content/uploads/2021/11/1-1-Aspect-Ratio-1024x1024.jpg"
            },
        )
        handler.endElement("itunes:image")
        handler.addQuickElement("itunes:category", "Arts")  # Modify this line
        handler.addQuickElement(
            "itunes:category", "Games & Hobbies > Video Games"
        )  # Modify this line
        handler.addQuickElement(
            "itunes:category", "News & Politics"
        )  # Modify this line
        handler.addQuickElement("language", "en-us")
        handler.addQuickElement(
            "lastBuildDate",
            datetime.datetime.now().strftime("%a, %d %b %Y %H:%M:%S %z"),
        )
        handler.startElement("itunes:owner", {})
        handler.addQuickElement("itunes:name", "Radio Frequenza Libera")
        handler.addQuickElement("itunes:email", "rfl.radiofrequenzalibera@gmail.com")
        handler.endElement("itunes:owner")

class PodcastFeed(Feed):
    feed_type = iTunesPodcastsFeedGenerator
    title = "Podcast Radio Frequenza Libera - On demand"
    link = "/feed/rss/"
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

    def item_enclosure_cover(self, item):
        return item.cover_url

    # def item_pubdate(self, item):
    #     return (
    #         item.insert_time
    #     )  # Modify this line to return the publication date of the episode

    def item_guid(self, item):  # Add this method
        return str(item.id)

    def item_explicit(self, item):  # Add this method
        return "no"

    def item_pubdate(self, item):
        # hardcode the date for now
        return datetime.datetime.now()
