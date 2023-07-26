from django.shortcuts import render

# Create your views here.
import json
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt

import logging

from podcaster.models import Podcaster

logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger(__name__)

# Create your views here.
def home(request):
    return render(request, "home.html")

@csrf_exempt
def create_podcaster(request):
    if request.method == "POST":
        body = request.body.decode('utf-8')
        logger.info(body)
        data = json.loads(body) # the load method is used to parse a JSON string
        name = data.get("name")
        presentation = data.get("presentation")
        image = data.get("image")
        podcast = Podcaster.objects.create(name=name, presentation=presentation, image=image)
        return JsonResponse({"id": podcast.id, "name": podcast.name, "presentation": podcast.presentation, "image": podcast.image})
    else:
        return HttpResponseNotAllowed(["POST"])