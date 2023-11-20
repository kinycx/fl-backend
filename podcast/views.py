# Create your views here.
import os
import json
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import (
    get_object_or_404,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)

from logger import logger
from .models import Podcast, PodcastSerializer

from frequenza_libera.settings import BASE_DIR


class PodcastListCreateView(ListCreateAPIView):
    """View for listing and creating Podcasts (GET, POST)"""

    queryset = Podcast.objects.all()
    serializer_class = PodcastSerializer


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
