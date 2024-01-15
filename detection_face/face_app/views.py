from django.shortcuts import render
from face_app.models import *


def index(request):
    return render(request, 'face_app/index.html')
