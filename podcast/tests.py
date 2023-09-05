from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from logger import logger
from .models.podcast import Podcast

class PodcastAPITest(TestCase):
    """Running test cases for Podcast API
    
    python manage.py test podcast
    """
    # python manage.py test podcast

    def setUp(self):
        self.client = APIClient()

    def test_create_podcast(self):
        url = reverse('podcast-list-create')
        data = {
            "name": "Test Podcast",
            "description": "This is a test podcast",
            "duration": "00:30:00",
            # Add other required fields here
        }
        logger.debug("Test create podcast")
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Podcast.objects.count(), 1)
        self.assertEqual(Podcast.objects.get().name, 'Test Podcast')

    def test_get_podcast_list(self):
        url = reverse('podcast-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_podcast_detail(self):
        podcast = Podcast.objects.create(name="Sample Podcast", description="Sample description", duration="00:45:00")
        url = reverse('podcast-retrieve-update-destroy', kwargs={'pk': podcast.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Sample Podcast')

    def test_update_podcast(self):
        podcast = Podcast.objects.create(name="Sample Podcast", description="Sample description", duration="00:45:00")
        url = reverse('podcast-retrieve-update-destroy', kwargs={'pk': podcast.id})
        updated_data = {
            "name": "Updated Podcast",
            "description": "Updated description",
            "duration": "01:00:00",
            # Add other fields to update here
        }

        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Podcast.objects.get(pk=podcast.id).name, 'Updated Podcast')

    def test_delete_podcast(self):
        podcast = Podcast.objects.create(name="Sample Podcast", description="Sample description", duration="00:45:00")
        url = reverse('podcast-retrieve-update-destroy', kwargs={'pk': podcast.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Podcast.objects.count(), 0)
