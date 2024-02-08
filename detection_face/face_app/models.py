from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    # photo = models.ImageField(upload_to="img/profile/%Y/%m/%d/", blank=True, null=True, verbose_name="Фотография аватара")

    def __str__(self):
        return self.username


class FaceTrimUser(models.Model):
    face_photo = models.ImageField(upload_to="face_trim/%Y/%m/%d/", verbose_name="Фотография лица")
    users_id = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Обрезанная фотография пользователя'
        verbose_name_plural = 'Обрезанные фотографии пользователей'


class Feedback(models.Model):
    descriptions = models.TextField()
    users_id = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Обратная связь'
        verbose_name_plural = 'Обратная связь'
