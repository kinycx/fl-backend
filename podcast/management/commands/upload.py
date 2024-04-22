import json
from podcast.models import Podcast
from django.core.management.base import BaseCommand
from datetime import datetime


class Command(BaseCommand):
    help = "Loads a JSON file to the database"

    def add_arguments(self, parser):
        parser.add_argument("json_file", type=str, help="The JSON file to load")

    def handle(self, *args, **kwargs):
        json_file = kwargs["json_file"]
        with open(json_file) as f:
            data = json.load(f)

        for item in data:
            # Assuming the JSON file is a list of objects and each object is a record for YourModel
            Podcast.objects.create(
                title=item["title"],
                description=item["description"],
                insert_time=datetime.strptime(
                    item["insert_time"].split(" ")[0], "%Y-%m-%d"
                ).time(),
                audio_url=item["file_url"],
                cover_url="https://podcast-fl.s3.eu-north-1.amazonaws.com/podcast_covers/foto_profilo.jpg",
            )
