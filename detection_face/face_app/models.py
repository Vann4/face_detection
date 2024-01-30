from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    # photo = models.ImageField(upload_to="img/profile/%Y/%m/%d/", blank=True, null=True, verbose_name="Фотография аватара")
    nickname = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.username


class Data_user(models.Model):
    photo = models.ImageField(upload_to="img/face/%Y/%m/%d/", verbose_name="Фотография лица")
    users = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Данные пользователей'
        verbose_name_plural = 'Данные пользователей'
