from django.shortcuts import render

# Create your views here.
import json
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt

import logging

from subject.models import Subject

logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger(__name__)

# Create your views here.
def home(request):
    return render(request, "home.html")

@csrf_exempt
def create_subject(request):
    if request.method == "POST":
        body = request.body.decode('utf-8')
        logger.info(body)
        data = json.loads(body) # the load method is used to parse a JSON string
        name = data.get("name")
        description = data.get("description")
        subject = Subject.objects.create(name=name, description=description)
        return JsonResponse({"id": subject.id, "name": subject.name, "description": subject.description})
    else:
        return HttpResponseNotAllowed(["POST"])