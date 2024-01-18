from django.http import HttpResponse
from django.shortcuts import render
from face_app.models import *


def index(request):
    username = User.objects.all()
    data = {
        'username': username,
    }
    return render(request, 'face_app/index.html', data)


def date_user(request, user_id):
    return render(request, 'face_app/date.html')


def page_not_found(request, exception):
    return HttpResponse('<h1>Страница не найдена!</h1>')
