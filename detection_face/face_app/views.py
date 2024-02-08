from django.contrib.auth.views import LoginView
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from .models import *
import face_recognition
from PIL import Image, ImageDraw
import pickle

from .forms import LoginUserForm, RegisterUserForm, FeedbackForm, TrimmingPhotoForm


def index(request):
    username = User.objects.all()

    # def extracting_faces(img_path):
    #     count = 0
    #     faces = face_recognition.load_image_file(img_path)
    #     faces_locations = face_recognition.face_locations(faces)
    #
    #     for face_location in faces_locations:
    #         top, right, bottom, left = face_location
    #
    #         face_img = faces[top:bottom, left:right]
    #         pil_img = Image.fromarray(face_img)
    #         pil_img.save(f"face_app/dataset/{count}_face_img.jpg")
    #         count += 1
    #
    #     print(f"Found {count} face(s) in this photo")
    #
    # print(extracting_faces("face_app/dataset/regina_2.jpg"))

    # # print(compare_faces("dataset/regina_1.jpg", "dataset_from_video/regina_2.jpg"))
    # img1 = face_recognition.load_image_file("face_app/dataset/regina_1.jpg")
    # img1 = face_recognition.load_image_file("face_app/dataset/stat.png")
    # img1_encodings = face_recognition.face_encodings(img1)[0]
    # # print(img1_encodings)
    #
    # img2 = face_recognition.load_image_file("face_app/dataset/regina_2.jpg")
    # img2_encodings = face_recognition.face_encodings(img2)[0]
    #
    # result = face_recognition.compare_faces([img1_encodings], img2_encodings)
    # print(result)

    # # print(img2_encodings)
    #
    # result = face_recognition.compare_faces([img1_encodings], img2_encodings)
    # # print(result)
    #
    # if result[0]:
    #     print("Welcome to the club! :*")
    # else:
    #     print("Sorry, not today... Next!")

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
        'username': username,
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


def working_with_images(request):
    if request.method == "POST":
        form = TrimmingPhotoForm(request.POST, request.FILES)
        if form.is_valid():
            face = form.save(commit=False)  # создание объекта без сохранения в БД
            face.save()
            return render(request, 'face_app/working_with_images.html')
    else:
        form = TrimmingPhotoForm()
    return render(request, 'face_app/working_with_images.html', {'form': form})
