from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings

from podcast.models import Podcast
from podcast_collection.models import PodcastCollection


class PodcastModelTest(TestCase):
    def test_filename_validation_rejects_bad_chars(self):
        bad = SimpleUploadedFile("bad name.mp3", b"x")
        p = Podcast(title="Bad", description="d")
        p.audio_file = bad
        with self.assertRaises(Exception):  # noqa: B017
            p.full_clean()

    @override_settings(AUDIO_UPLOAD_FOLDER="audio/", AWS_S3_BUCKET_NAME="bucket")
    def test_audio_url_set_on_change_and_unescape(self):
        audio = SimpleUploadedFile("track.mp3", b"data")
        p = Podcast(title="A1", description="&amp;stuff", duration=10)
        p.audio_file = audio
        p.save()
        self.assertIn("bucket.s3.amazonaws.com", p.audio_url)
        self.assertEqual(p.description, "&stuff")

    def test_collection_update_time_modified_on_first_save(self):
        c = PodcastCollection.objects.create(title="Col X")
        old_update = c.update_time
        Podcast.objects.create(title="PC", description="d", duration=1, collection=c)
        c.refresh_from_db()
        self.assertNotEqual(old_update, c.update_time)
