from django.contrib.auth.views import LoginView
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .models import *
import face_recognition
from PIL import Image, ImageDraw
import pickle
from pathlib import Path
from deepface import DeepFace

from .forms import LoginUserForm, RegisterUserForm, FeedbackForm, TrimmingPhotoForm, AgeGenderRaceForm


def index(request):
    users = User.objects.all()

    # img1 = face_recognition.load_image_file("face_app/media/0_Katya.jpg")
    # img1_encodings = face_recognition.face_encodings(img1)[0]
    #
    # img2 = face_recognition.load_image_file("face_app/media/0_Katya.jpg")
    # img2_encodings = face_recognition.face_encodings(img2)[0]
    #
    # result = face_recognition.compare_faces([img1_encodings], img2_encodings)
    # print(result)
    #
    # if result[0]:
    #     print("Добро пожаловать!!!")
    # else:
    #     print("Извините, не сегодня")

    # context = {}

    # if result[0]:
    #     context['welcome_text'] = "Welcome to the club!"
    #     # aa = {'a': 'fgfg'}
    #     # aa = 'fg'
    # else:
    #     context['sorry_text'] = "Sorry, not today..."

    if request.method == "POST":
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)  # создание объекта без сохранения в БД
            feedback.save()
    else:
        form = FeedbackForm()

    data = {
        'users': users,
        'form': form,
        # 'context': context,
        # 'aa': aa,
    }
    return render(request, 'face_app/index.html', data)


def page_not_found(request, exception):
    return HttpResponse('<h1>Страница не найдена!</h1>')


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'face_app/login.html'
    extra_context = {'title': "Авторизация"}

    def get_success_url(self):
        return reverse_lazy('index')


def registration(request):
    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # создание объекта без сохранения в БД
            # user.username = compare_faces("face_app/dataset/regina_1.jpg", "face_app/dataset/regina_2.jpg")
            # data = request.POST.get('email', None)
            # print(data)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return render(request, 'face_app/registration_done.html')
    else:
        form = RegisterUserForm()
    return render(request, 'face_app/registration.html', {'form': form})


def working_with_images(request, users_id):
    path_img = ''
    ResultDeepAnalyze = {}
    face_user = FaceTrimUser.objects.filter(users_id=users_id)
    form1 = TrimmingPhotoForm(request.POST, request.FILES or None)
    form2 = AgeGenderRaceForm(request.POST)

    if users_id == request.user.id:
        if request.method == "POST":
            # form = TrimmingPhotoForm(request.POST, request.FILES)
            if form1.is_valid():
                face = form1.save(commit=False)  # создание объекта без сохранения в БД

                count = 0
                faces = face_recognition.load_image_file(face.face_photo)
                faces_locations = face_recognition.face_locations(faces)

                face_trim = f"{face.face_photo}"
                print(face_trim)

                for face_location in faces_locations:
                    top, right, bottom, left = face_location

                    face_img = faces[top:bottom, left:right]
                    pil_img = Image.fromarray(face_img)
                    pil_img.save(f"face_app/media/{count}_{face_trim}")
                    face_user_photo = FaceTrimUser(face_photo=f"{count}_{face_trim}", users_id=face.users_id)
                    face_user_photo.save()
                    count += 1

            if form2.is_valid():
                path_img = form2.cleaned_data['path']
                image_path = Path(f"face_app/media/{path_img}")
                DeepAnalyze = DeepFace.analyze(img_path=image_path, actions=['age', 'gender', 'race', 'emotion'], enforce_detection=False)
                ResultDeepAnalyze = DeepAnalyze[0]
        else:
            form1 = TrimmingPhotoForm()
            form2 = AgeGenderRaceForm()

        data = {
            'face_user': face_user,
            'form1': form1,
            'form2': form2,
            'ResultDeepAnalyze': ResultDeepAnalyze,
            'path_img': path_img,
        }

        return render(request, 'face_app/working_with_images.html', data)
    else:
        raise PermissionDenied
