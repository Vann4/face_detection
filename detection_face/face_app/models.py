from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    # photo = models.ImageField(upload_to="img/profile/%Y/%m/%d/", blank=True, null=True, verbose_name="Фотография аватара")

    def __str__(self):
        return self.username


class FaceTrimUser(models.Model):
    face_photo = models.ImageField(verbose_name="Фотография лица")
    name = models.TextField(blank=True, null=True, verbose_name="Имя")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")
    age = models.IntegerField(blank=True, null=True, verbose_name="Возраст")
    dominant_gender = models.CharField(blank=True, null=True, max_length=10, verbose_name="Пол")
    dominant_race = models.CharField(blank=True, null=True, max_length=100, verbose_name="Раса")
    dominant_emotion = models.CharField(blank=True, null=True, max_length=100, verbose_name="Эмоция")
    face_encodings = models.BinaryField(blank=True, null=True, verbose_name="Кодировка лиц")
    download_date = models.DateField(auto_now=True)
    users_id = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Фотография пользователя'
        verbose_name_plural = 'Фотографии пользователей'

    def __str__(self):
        return self.face_photo.url


class Feedback(models.Model):
    descriptions = models.TextField()
    users_id = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Обратная связь'
        verbose_name_plural = 'Обратная связь'

    def __str__(self):
        return self.descriptions
