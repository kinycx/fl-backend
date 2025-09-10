from rest_framework.generics import (
    ListCreateAPIView,
)

from .models import PodcastCollection, PodcastCollectionSerializer


class PodcastCollectionListCreateView(ListCreateAPIView):
    """View for listing and creating Podcasts (GET, POST)"""

    queryset = PodcastCollection.objects.all().order_by("-update_time")
    serializer_class = PodcastCollectionSerializer
