# Create your views here.
import json
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
from rest_framework.generics import get_object_or_404, ListCreateAPIView, RetrieveUpdateDestroyAPIView

from logger import logger
from ..models.podcast import Podcast, PodcastSerializer

class PodcastListCreateView(ListCreateAPIView):
    """View for listing and creating Podcasts (GET, POST)"""
    queryset = Podcast.objects.all()
    serializer_class = PodcastSerializer

class PodcastRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    """View for retrieving, updating and deleting Podcasts (GET, PUT, DELETE)"""
    queryset = Podcast.objects.all()
    serializer_class = PodcastSerializer