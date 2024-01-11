# Create your views here.
import os
import json
from django.http import FileResponse, HttpResponse
from django.views import View
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
from services.stream import generate_feed

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


# TODO: edit to take mp3 file from s3 bucket
class ServeAudioView(View):
    def get(self, request):
        filepath = request.GET.get("filepath")
        return FileResponse(open(filepath, "rb"))


class ServeRSSView(View):
    def get(self, request):
        base_url = "http://example.com/"
        audio_path = "episode1.mp3"
        description = "This is the first episode of my podcast"
        rssfeed = generate_feed(base_url, audio_path, description)
        return HttpResponse(rssfeed, content_type="application/rss+xml")
