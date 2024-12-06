from django.core.management.base import BaseCommand
from podcast.models import Podcast
import html


class Command(BaseCommand):
    help = "Remove duplicate Podcast entries based on title and unescape HTML entities in descriptions"

    def handle(self, *args, **kwargs):
        # Find all unique titles
        unique_titles = set()
        duplicates = []

        for podcast in Podcast.objects.all():
            # Unescape HTML entities in the description
            old_description = podcast.description
            podcast.description = html.unescape(podcast.description)
            if podcast.description != old_description:
                self.stdout.write(
                    self.style.SUCCESS(f"Unescaped HTML entities in {podcast.title}")
                )
                podcast.save()

            if podcast.title in unique_titles:
                duplicates.append(podcast.id)
            else:
                unique_titles.add(podcast.title)

        # Delete duplicates
        if duplicates:
            Podcast.objects.filter(id__in=duplicates).delete()
            self.stdout.write(
                self.style.SUCCESS(f"Deleted {len(duplicates)} duplicate entries")
            )
        else:
            self.stdout.write(self.style.SUCCESS("No duplicates found"))
