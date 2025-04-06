from rest_framework.generics import (
    get_object_or_404,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)

from .models import PodcastCollection, PodcastCollectionSerializer



class PodcastCollectionListCreateView(ListCreateAPIView):
    """View for listing and creating Podcasts (GET, POST)"""

    queryset = PodcastCollection.objects.all()
    serializer_class = PodcastCollectionSerializer
