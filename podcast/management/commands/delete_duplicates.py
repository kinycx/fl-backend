from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError
from podcast.models import Podcast
import html
import re


class Command(BaseCommand):
    help = "Remove duplicate Podcast entries based on title and description, and unescape HTML entities in descriptions"

    def handle(self, *args, **kwargs):
        # Find all unique (title, description) pairs
        unique_entries = set()
        duplicates = []

        for podcast in Podcast.objects.all():
            # Unescape HTML entities in the description
            old_description = podcast.description
            podcast.description = html.unescape(podcast.description)
            # Remove leading and trailing whitespace and replace multiple spaces with a single space
            podcast.description = re.sub(r"\s+", " ", podcast.description.strip())
            if podcast.description != old_description:
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Unescaped HTML entities and normalized whitespace in {podcast.title}"
                    )
                )

            # Normalize title
            old_title = podcast.title
            podcast.title = re.sub(r"\s+", " ", podcast.title.strip())
            if podcast.title != old_title:
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Normalized whitespace in title: {podcast.title}"
                    )
                )

            entry = (podcast.title, podcast.description)
            if entry in unique_entries:
                duplicates.append(podcast.id)
            else:
                unique_entries.add(entry)
                # Save only if the entry is unique
                try:
                    podcast.save()
                except IntegrityError:
                    self.stdout.write(
                        self.style.ERROR(
                            f"Failed to save {podcast.title} due to unique constraint violation"
                        )
                    )
                    duplicates.append(podcast.id)

        # Delete duplicates
        if duplicates:
            Podcast.objects.filter(id__in=duplicates).delete()
            self.stdout.write(
                self.style.SUCCESS(f"Deleted {len(duplicates)} duplicate entries")
            )
        else:
            self.stdout.write(self.style.SUCCESS("No duplicates found"))
