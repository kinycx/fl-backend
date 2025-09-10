from django.conf import settings
from django.utils.feedgenerator import Rss201rev2Feed

bucket_url = f"https://{settings.AWS_S3_BUCKET_NAME}.s3.{settings.AWS_REGION}.amazonaws.com/"


class iTunesPodcastsFeedGenerator(Rss201rev2Feed):
    def rss_attributes(self):
        return {
            "version": self._version,
            "xmlns:itunes": "http://www.itunes.com/dtds/podcast-1.0.dtd",
            "xmlns:atom": "http://www.w3.org/2005/Atom",
        }

    def add_item_elements(self, handler, item):
        # Call default behavior
        super().add_item_elements(handler, item)

        # Add enclosure tag if values provided.
        if item.get("enclosure_url"):
            attributes = {
                "url": item["enclosure_url"],
                "length": str(item.get("enclosure_length", 0)),
                "type": item.get("enclosure_mime_type", "audio/mpeg"),
            }
            handler.addQuickElement("enclosure", "", attributes)

        # Add itunes:image if provided.
        if item.get("enclosure_cover"):
            handler.startElement("itunes:image", {"href": item["enclosure_cover"]})
            handler.endElement("itunes:image")

    def add_root_elements(self, handler):
        super().add_root_elements(handler)
        handler.addQuickElement(
            "managingEditor",
            settings.EMAIL,
        )

        handler.addQuickElement("itunes:author", "Radio Frequenza Libera")
        handler.addQuickElement("itunes:explicit", "false")
        handler.startElement(
            "itunes:image",
            {"href": f"{bucket_url}podcast_media_generics/foto+profilo.jpg"},
        )
        handler.endElement("itunes:image")
        handler.startElement("itunes:category", {"text": "Arts"})
        handler.endElement("itunes:category")
        handler.startElement("itunes:category", {"text": "Games & Hobbies"})
        handler.endElement("itunes:category")
        handler.startElement("itunes:category", {"text": "Government"})
        handler.endElement("itunes:category")
        handler.startElement("itunes:owner", {})
        handler.addQuickElement("itunes:name", "Radio Frequenza Libera")
        handler.addQuickElement("itunes:email", settings.EMAIL)
        handler.endElement("itunes:owner")
