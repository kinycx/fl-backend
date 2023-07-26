import json
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt

import logging

from .models import Podcast

logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger(__name__)

# Create your views here.
def home(request):
    return render(request, "home.html")

@csrf_exempt
def create_podcast(request):
    if request.method == "POST":
        body = request.body.decode('utf-8')
        logger.info(body)
        data = json.loads(body) # the load method is used to parse a JSON string
        name = data.get("name")
        description = data.get("description")
        podcast = Podcast.objects.create(name=name, description=description)
        return JsonResponse({"id": podcast.id, "name": podcast.name, "description": podcast.description})
    else:
        return HttpResponseNotAllowed(["POST"])