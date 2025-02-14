import os
import json

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import (
    get_object_or_404,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)

from logger import logger
from .models import PodcastCollection, PodcastCollectionSerializer
from .pagination import PodcastCollectionPagination

from frequenza_libera.settings import BASE_DIR


class PodcastCollectionListCreateView(ListCreateAPIView):
    """View for listing and creating Podcasts (GET, POST)"""

    queryset = PodcastCollection.objects.all()
    serializer_class = PodcastCollectionSerializer
    pagination_class = PodcastCollectionPagination
