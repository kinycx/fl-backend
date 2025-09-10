# Create your views here.
import json
import os
import random

from rest_framework import status
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.response import Response
from rest_framework.views import APIView

from frequenza_libera.settings import BASE_DIR
from logger import logger

from .models import Podcast, PodcastSerializer
from .pagination import PodcastPagination


class PodcastListByCollectionCreateView(ListCreateAPIView):
    """View for listing and creating Podcasts by Collection (GET, POST)"""

    queryset = Podcast.objects.all().order_by("insert_time")
    serializer_class = PodcastSerializer

    def get_queryset(self):
        collection = self.kwargs["collection"]
        return Podcast.objects.filter(collection=collection).order_by("insert_time")

    def post(self, request, *args, **kwargs):
        collection = self.kwargs["collection"]
        logger.info(f"Creating Podcast in Collection {collection}")
        return super().post(request, *args, **kwargs)


class PodcastListCreatePaginatedView(ListCreateAPIView):
    """View for listing and creating Podcasts (GET, POST)"""

    queryset = Podcast.objects.all().order_by("-insert_time")
    serializer_class = PodcastSerializer
    pagination_class = PodcastPagination


class PodcastRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    """View for retrieving, updating and deleting Podcasts (GET, PUT, DELETE)"""

    queryset = Podcast.objects.all()
    serializer_class = PodcastSerializer


class BulkCreatePodcastView(APIView):
    """View for bulk creating Podcasts (GET)"""

    def get(self, request, *args, **kwargs):
        with open(os.path.join(BASE_DIR, "feed.json")) as json_file:
            data = json.load(json_file)
            for podcast in data:
                Podcast.objects.create(
                    title=podcast["title"],
                    description=podcast["description"],
                    audio_url=podcast["audio_url"],
                    insert_time=podcast["insert_time"],
                )
        return Response({"message": "Podcasts created successfully"}, status=201)


class RandomPodcastView(APIView):
    """Return a single random Podcast (optionally filtered by ?collection=<uuid>)"""

    def get(self, request, *args, **kwargs):
        qs = Podcast.objects.all()
        collection = request.query_params.get("collection")
        if collection:
            qs = qs.filter(collection=collection)
        count = qs.count()
        if count == 0:
            return Response({"detail": "No podcast found"}, status=status.HTTP_404_NOT_FOUND)
        podcast = qs[random.randint(0, count - 1)]
        data = PodcastSerializer(podcast).data
        return Response(data, status=status.HTTP_200_OK)
