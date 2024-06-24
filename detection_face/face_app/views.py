import os

from django.contrib.auth import get_user_model, authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.core.exceptions import PermissionDenied
from django.core.files.base import ContentFile
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import UpdateView

from .models import *
import face_recognition
from PIL import Image
from pathlib import Path
from deepface import DeepFace
import numpy as np
import cv2
import time

from django.http import StreamingHttpResponse
from django.views.decorators import gzip


from .forms import LoginUserForm, RegisterUserForm, FeedbackForm, TrimmingPhotoForm, AgeGenderRaceForm, \
    UpdateDataPhotoForm, DeletePhotoForm, FilterForDataOutputForm, UserProfileForm, UserPasswordChangeForm


def feedback(request):
    if request.method == "POST":
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)  # создание объекта без сохранения в БД
            feedback.save()
            return JsonResponse({'message': 'Данные успешно сохранены'}, status=200)
        else:
            return JsonResponse({'message': 'Что-то пошло не так'}, status=400)


def index(request):
    return render(request, 'face_app/index.html')


def page_not_found(request, exception):
    return HttpResponse('<h1>Страница не найдена!</h1>')


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'face_app/login.html'
    extra_context = {'title': "Авторизация"}

    def get_success_url(self):
        return reverse_lazy('user_profile')


def registration(request):
    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # создание объекта без сохранения в БД
            user.set_password(form.cleaned_data['password'])
            user.save()

            username = request.POST['username']
            password = request.POST['password']

            # Аутентификация пользователя
            user = authenticate(request, username=username, password=password)

            if user is not None:
                # Если пользователь успешно аутентифицирован, выполняем вход
                login(request, user)
                url = reverse('user_profile')
                return HttpResponseRedirect(url)
            else:
                url = reverse('login')
                return HttpResponseRedirect(url)
    else:
        form = RegisterUserForm()
    return render(request, 'face_app/registration.html', {'form': form})


class UserProfile(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    form_class = UserProfileForm
    template_name = 'face_app/user_profile.html'
    extra_context = {'title': "Профиль пользователя"}

    def get_success_url(self):
        return reverse_lazy('user_profile')

    def get_object(self, queryset=None):
        return self.request.user


class UserPasswordChange(PasswordChangeView):
    form_class = UserPasswordChangeForm
    success_url = reverse_lazy("password_change_done")
    template_name = "face_app/password_change_form.html"


known_face_encodings = []
known_face_names = []
known_face_ids = []

face_locations = []
face_encodings = []
face_names = []


def gen(camera, users_id):
    face_user = FaceTrimUser.objects.filter(users_id=users_id).order_by('id')
    users_id = User.objects.get(id=users_id)
    for data_face_user in face_user:
        face_encoding = np.frombuffer(data_face_user.face_encodings, dtype=np.float64)
        known_face_encodings.append(face_encoding)
        known_face_names.append(data_face_user.name)
        known_face_ids.append(data_face_user.id)

    process_this_frame = True
    while True:
        ret, frame = camera.read()
        if not ret:
            break
        else:
            if process_this_frame:
                # Изменение размера кадра видео до 1 / 4 для более быстрой обработки распознавания лиц
                small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

                # Преобразование изображения из цвета BGR (который использует OpenCV) в цвет RGB (который использует face_recognition)
                rgb_small_frame = small_frame[:, :, ::-1]

                # Найти все лица и кодировки лиц в текущем кадре видео
                face_locations = face_recognition.face_locations(rgb_small_frame)
                face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

                face_names = []
                for face_encoding, face_location in zip(face_encodings, face_locations):
                    # Проверить, совпадает ли лицо с известным лицом (лицами).
                    # matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                    name = "Неизвестно"
                    face_id = None

                    # Или вместо этого использовать известное лицо с наименьшим расстоянием до нового лица
                    # face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                    # best_match_index = int(np.argmin(face_distances))
                    # if matches[best_match_index]:
                    #     name = known_face_names[best_match_index]
                    #     face_id = known_face_ids[best_match_index]

                    if known_face_encodings:
                        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                        best_match_index = int(np.argmin(face_distances))
                        if matches[best_match_index]:
                            name = known_face_names[best_match_index]
                            face_id = known_face_ids[best_match_index]

                    # Масштабирование местоположение лиц
                    top, right, bottom, left = face_location
                    top *= 4
                    right *= 4
                    bottom *= 4
                    left *= 4

                    # Извлечение изображения лица
                    face_image = frame[top:bottom, left:right]
                    _, buffer = cv2.imencode('.jpg', face_image)
                    face_image_file = ContentFile(buffer.tobytes())

                    if face_id is not None and FaceTrimUser.objects.filter(id=face_id).exists():
                        # Если лицо известно, сохранить запись с известной информацией
                        matched_face_user = FaceTrimUser.objects.get(id=face_id)
                        face_record = FaceTrimUser(
                            face_encodings=face_encoding.tobytes(),
                            name=name,
                            description=matched_face_user.description,
                            age=matched_face_user.age,
                            dominant_gender=matched_face_user.dominant_gender,
                            dominant_race=matched_face_user.dominant_race,
                            dominant_emotion=matched_face_user.dominant_emotion,
                            users_id=users_id
                        )
                    else:
                        # Если лицо неизвестно, создать новую запись с кодировкой лица
                        face_record = FaceTrimUser(
                            face_encodings=face_encoding.tobytes(),
                            name=name,
                            users_id=users_id
                        )

                    record = FaceTrimUser.objects.order_by('-id').first()
                    face_record.face_photo.save(f'face_{record.id + 1}.jpg', face_image_file)
                    face_record.save()
                    face_names.append(name)
                    # Задержка перед сохранением записи
                    time.sleep(0.5)
            process_this_frame = not process_this_frame

            # Отображение результатов
            for (top, right, bottom, left), name in zip(face_locations, face_names):
                # Масштабирование местоположение лиц, поскольку кадр, в котором мы находились, был масштабирован до 1/4 размера
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4

                # Рамка вокруг лица
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

                # Рамка с именем под лицом
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                font = cv2.FONT_HERSHEY_COMPLEX
                cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

            # Конвертирование изображения в формат JPEG
            _, jpeg = cv2.imencode('.jpg', frame)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n')


@gzip.gzip_page
def live_feed(request, users_id):
    try:
        camera = cv2.VideoCapture(0)
    except Exception:
        pass

    return StreamingHttpResponse(gen(camera, users_id), content_type="multipart/x-mixed-replace;boundary=frame")


def extracting_faces(faces, face_user, users_id, count, id_photo_user, file_extension):
    face_encoding_user_upload = face_recognition.face_encodings(faces)[0]
    FaceTrimUser.objects.filter(users_id=users_id, face_photo=f"{count}_image_{id_photo_user}{file_extension}").update(face_encodings=face_encoding_user_upload)

    for data_face_user in face_user:
        face_encoding = np.frombuffer(data_face_user.face_encodings, dtype=np.float64)
        result = face_recognition.compare_faces([face_encoding],
                                                face_encoding_user_upload)  # Сравнение кодировок лиц из базы данных с загруженным
        if result[0]:
            FaceTrimUser.objects.filter(users_id=users_id, face_photo=f"{count}_image_{id_photo_user}{file_extension}").update(
                name=data_face_user.name,
                description=data_face_user.description,
                age=data_face_user.age,
                dominant_gender=data_face_user.dominant_gender,
                dominant_race=data_face_user.dominant_race)
            break
        else:
            pass


def get_file_extension(file_path):
    _, extension = os.path.splitext(file_path)
    return extension


def working_with_images(request, users_id):
    global id_photo_user
    face_user = FaceTrimUser.objects.filter(users_id=users_id).order_by('id')

    form1 = TrimmingPhotoForm(request.POST, request.FILES)
    form2 = AgeGenderRaceForm(request.POST)
    UpdateDataPhoto = UpdateDataPhotoForm(request.POST)
    DeletePhoto = DeletePhotoForm(request.POST)
    FilterForDataOutput = FilterForDataOutputForm(request.POST)

    if users_id == request.user.id:
        if request.method == "POST":
            if form1.is_valid():

                face = form1.save(commit=False)  # создание объекта без сохранения в БД
                count = 0
                faces = face_recognition.load_image_file(face.face_photo)
                faces_locations = face_recognition.face_locations(faces)

                face_trim = f"{face.face_photo}"

                file_extension = get_file_extension(face_trim)  # Получение расширения изображения

                for face_location in faces_locations:
                    top, right, bottom, left = face_location

                    face_img = faces[top:bottom, left:right]
                    face_user_photo = FaceTrimUser(face_photo=f"{count}_test{file_extension}", users_id=face.users_id)
                    face_user_photo.save()

                    update_name_photo = FaceTrimUser.objects.filter(face_photo=f"{count}_test{file_extension}", users_id=users_id)
                    for obj_face_user_photo in update_name_photo:
                        id_photo_user = obj_face_user_photo.id
                        FaceTrimUser.objects.filter(users_id=users_id, face_photo=f"{count}_test{file_extension}").update(face_photo=f'{count}_image_{id_photo_user}{file_extension}')
                        pil_img = Image.fromarray(face_img)
                        pil_img.save(f"face_app/media/{count}_image_{obj_face_user_photo.id}{file_extension}")

                    extracting_faces(faces, face_user, users_id, count, id_photo_user, file_extension)
                    count += 1
                url = reverse('working_with_images', args=[users_id])
                return HttpResponseRedirect(url)

            if form2.is_valid():
                path_img = form2.cleaned_data['path']
                image_path = Path(f"face_app/media/{path_img}")
                DeepAnalyze = DeepFace.analyze(img_path=image_path, actions=['age', 'gender', 'race', 'emotion'],
                                               enforce_detection=False)
                ResultDeepAnalyze = DeepAnalyze[0]

                gender_translation = {'Man': 'Мужчина', 'Woman': 'Женщина'}

                race_translation = {'indian': 'Индейцы', 'Asian': 'Азиаты',
                                    'latino hispanic': 'Латиноамериканцы', 'black': 'Африканцы',
                                    'middle eastern': 'Средневосточная', 'white': 'Европейцы'}

                emotion_translation = {'happy': 'Счастье', 'sad': 'Грусть',
                                       'angry': 'Гнев', 'surprise': 'Удивление', 'fear': 'Страх',
                                       'disgust': 'Отвращение', 'neutral': 'Нет эмоций'}

                ResultDeepAnalyze['dominant_gender'] = gender_translation.get(ResultDeepAnalyze['dominant_gender'],
                                                                              ResultDeepAnalyze['dominant_gender'])
                ResultDeepAnalyze['dominant_race'] = race_translation.get(ResultDeepAnalyze['dominant_race'],
                                                                          ResultDeepAnalyze['dominant_race'])
                ResultDeepAnalyze['dominant_emotion'] = emotion_translation.get(ResultDeepAnalyze['dominant_emotion'],
                                                                                ResultDeepAnalyze['dominant_emotion'])

                FaceTrimUser.objects.filter(users_id=users_id, face_photo=path_img).update(age=ResultDeepAnalyze['age'],
                                                                                           dominant_gender=
                                                                                           ResultDeepAnalyze[
                                                                                               'dominant_gender'],
                                                                                           dominant_race=
                                                                                           ResultDeepAnalyze[
                                                                                               'dominant_race'],
                                                                                           dominant_emotion=
                                                                                           ResultDeepAnalyze[
                                                                                               'dominant_emotion'])
                url = reverse('working_with_images', args=[users_id])
                return HttpResponseRedirect(url)

            if UpdateDataPhoto.is_valid():  # Сохранение изменений, которые вносит пользователь через форму
                id_photo = UpdateDataPhoto.cleaned_data['id_photo']
                name = UpdateDataPhoto.cleaned_data['name']
                description = UpdateDataPhoto.cleaned_data['description']
                age = UpdateDataPhoto.cleaned_data['age']
                dominant_gender = UpdateDataPhoto.cleaned_data['dominant_gender']
                dominant_race = UpdateDataPhoto.cleaned_data['dominant_race']
                dominant_emotion = UpdateDataPhoto.cleaned_data['dominant_emotion']

                FaceTrimUser.objects.filter(id=id_photo, users_id=users_id).update(
                    name=name,
                    description=description,
                    age=age,
                    dominant_gender=dominant_gender,
                    dominant_race=dominant_race,
                    dominant_emotion=dominant_emotion)
                url = reverse('working_with_images', args=[users_id])
                return HttpResponseRedirect(url)

            if DeletePhoto.is_valid():  # удаление фото
                id = DeletePhoto.cleaned_data['id']
                name_photo = FaceTrimUser.objects.filter(id=id, users_id=users_id)
                for obj_face_name_user_photo in name_photo:
                    file_path = f'face_app/media/{obj_face_name_user_photo.face_photo}'
                    os.remove(file_path)
                name_photo.delete()
                url = reverse('working_with_images', args=[users_id])
                return HttpResponseRedirect(url)

            if FilterForDataOutput.is_valid():  # Фильтр для вывода данных
                name_filter = FilterForDataOutput.cleaned_data['name_filter']
                description_filter = FilterForDataOutput.cleaned_data['description_filter']
                age_filter = FilterForDataOutput.cleaned_data['age_filter']
                dominant_gender_filter = FilterForDataOutput.cleaned_data['dominant_gender_filter']
                dominant_race_filter = FilterForDataOutput.cleaned_data['dominant_race_filter']
                dominant_emotion_filter = FilterForDataOutput.cleaned_data['dominant_emotion_filter']
                download_date_filter = FilterForDataOutput.cleaned_data['download_date_filter']
                start_date = FilterForDataOutput.cleaned_data['start_date']
                end_date = FilterForDataOutput.cleaned_data['end_date']

                filtered_face_trim_user = FaceTrimUser.objects.filter(
                    Q(name=name_filter) | Q(description=description_filter) | Q(age=age_filter)
                    | Q(dominant_gender=dominant_gender_filter)
                    | Q(dominant_race=dominant_race_filter)
                    | Q(dominant_emotion=dominant_emotion_filter)
                    | Q(download_date=download_date_filter)
                    | Q(download_date__range=(start_date, end_date)),
                    users_id=users_id)

                data = {
                    'filtered_face_trim_user': filtered_face_trim_user,
                    'FilterForDataOutput': FilterForDataOutput
                }

                return render(request, 'face_app/working_with_images.html', data)

        else:
            form1 = TrimmingPhotoForm()
            form2 = AgeGenderRaceForm()
            UpdateDataPhoto = UpdateDataPhotoForm()
            DeletePhoto = DeletePhotoForm()
            FilterForDataOutput = FilterForDataOutputForm()

        data = {
            'face_user': face_user,
            'form1': form1,
            'form2': form2,
            'UpdateDataPhoto': UpdateDataPhoto,
            'DeletePhoto': DeletePhoto,
            'FilterForDataOutput': FilterForDataOutput
        }

        return render(request, 'face_app/working_with_images.html', data)
    else:
        raise PermissionDenied


def stats(request):
    return render(request, 'face_app/stats.html')
