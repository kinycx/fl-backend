from django.shortcuts import render
import time

# Create your views here.
import json
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt

import logging

from collection.models import Collection

logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger(__name__)

# Create your views here.
def home(request):
    return render(request, "home.html")

@csrf_exempt
def create_collection(request):
    if request.method == "POST":
        body = request.body.decode('utf-8')
        logger.info(body)
        data = json.loads(body) # the load method is used to parse a JSON string
        name = data.get("name")
        description = data.get("description")
        collection = Collection.objects.create(name=name, description=description)
        return JsonResponse({"id": collection.id, "name": collection.name, "description": collection.description})
    else:
        return HttpResponseNotAllowed(["POST"])