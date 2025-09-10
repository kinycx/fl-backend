from django.test import TestCase
from django.urls import reverse

from podcast.models import Podcast


class RandomPodcastViewTest(TestCase):
    def test_random_empty(self):
        url = reverse("podcast-random")
        r = self.client.get(url)
        self.assertEqual(r.status_code, 404)

    def test_random_returns_one(self):
        Podcast.objects.create(title="A", description="d", duration=1)
        Podcast.objects.create(title="B", description="d", duration=1)
        url = reverse("podcast-random")
        r = self.client.get(url)
        self.assertEqual(r.status_code, 200)
        self.assertIn(r.data["title"], {"A", "B"})
