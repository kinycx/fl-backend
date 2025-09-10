from unittest.mock import patch

from django.test import TestCase, override_settings
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from podcast.models import Podcast
from podcast_collection.models import PodcastCollection
from podcaster.models import Podcaster


class PodcastAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.collection = PodcastCollection.objects.create(title="Collection A")

    def create_podcast(self, **kwargs):
        return Podcast.objects.create(
            title=kwargs.get("title", "Podcast Title"),
            description=kwargs.get("description", "Desc"),
            duration=kwargs.get("duration", 120),
            collection=self.collection if kwargs.get("with_collection", True) else None,
        )

    def test_create_and_retrieve_podcast(self):
        url = reverse("podcast-list-create")
        payload = {
            "title": "P1",
            "description": "D1",
            "duration": 60,
            "collection": str(self.collection.id),
        }
        r = self.client.post(url, payload, format="json")
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)
        pid = r.data["id"]
        detail = reverse("podcast-retrieve-update-destroy", kwargs={"pk": pid})
        r2 = self.client.get(detail)
        self.assertEqual(r2.status_code, status.HTTP_200_OK)
        self.assertEqual(r2.data["title"], "P1")

    def test_list_pagination(self):
        for i in range(15):
            Podcast.objects.create(title=f"T{i}", description="d", duration=10)
        url = reverse("podcast-list-create")
        r = self.client.get(url)
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(len(r.data["results"]), 10)
        r2 = self.client.get(url + "?page=2")
        self.assertEqual(len(r2.data["results"]), 5)

    def test_update_and_delete(self):
        p = self.create_podcast(title="ToUpdate")
        detail = reverse("podcast-retrieve-update-destroy", kwargs={"pk": p.id})
        r = self.client.put(
            detail,
            {
                "title": "Updated",
                "description": "New",
                "duration": 300,
                "collection": str(self.collection.id),
            },
            format="json",
        )
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.data["title"], "Updated")
        r2 = self.client.delete(detail)
        self.assertEqual(r2.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Podcast.objects.filter(id=p.id).count(), 0)

    def test_list_by_collection(self):
        other = PodcastCollection.objects.create(title="Other")
        p1 = self.create_podcast(title="InCol")
        Podcast.objects.create(title="NoCol", description="d", duration=10)
        Podcast.objects.create(title="OtherCol", description="d", duration=10, collection=other)
        url = reverse(
            "podcast-list-by-collection-create", kwargs={"collection": str(self.collection.id)}
        )
        r = self.client.get(url)
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        ids = {item["id"] for item in r.data}
        self.assertIn(str(p1.id), ids)

    def test_random_endpoint_basic(self):
        url = reverse("podcast-random")
        r = self.client.get(url)
        self.assertEqual(r.status_code, status.HTTP_404_NOT_FOUND)
        self.create_podcast(title="R1")
        self.create_podcast(title="R2")
        r2 = self.client.get(url)
        self.assertEqual(r2.status_code, status.HTTP_200_OK)
        self.assertIn(r2.data["title"], {"R1", "R2"})

    def test_random_endpoint_collection_filter(self):
        other = PodcastCollection.objects.create(title="Other")
        self.create_podcast(title="C1")
        Podcast.objects.create(title="OC1", description="d", duration=1, collection=other)
        url = reverse("podcast-random") + f"?collection={self.collection.id}"
        titles = set()
        for _ in range(5):
            r = self.client.get(url)
            self.assertEqual(r.status_code, status.HTTP_200_OK)
            titles.add(r.data["title"])
        self.assertTrue(titles.issubset({"C1"}))

    def test_add_podcasters(self):
        p = self.create_podcast(title="WithHosts")
        host1 = Podcaster.objects.create(name="Alice")
        host2 = Podcaster.objects.create(name="Bob")
        p.podcasters.add(host1, host2)
        self.assertEqual(p.podcasters.count(), 2)

    def test_serializer_returns_all_fields(self):
        p = self.create_podcast(title="Ser")
        url = reverse("podcast-retrieve-update-destroy", kwargs={"pk": p.id})
        r = self.client.get(url)
        for field in ["id", "title", "description", "duration", "insert_time"]:
            self.assertIn(field, r.data)

    @override_settings(DEBUG=False)
    @patch("podcast.signals.call_command")
    def test_signal_triggers_feed_generation_in_prod(self, mock_call):
        Podcast.objects.create(title="SigPod", description="d", duration=1)
        self.assertTrue(mock_call.called)

    @override_settings(DEBUG=True)
    @patch("podcast.signals.call_command")
    def test_signal_skips_feed_generation_in_debug(self, mock_call):
        Podcast.objects.create(title="SigPod2", description="d", duration=1)
        self.assertFalse(mock_call.called)
