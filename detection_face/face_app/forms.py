from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm

from .models import Feedback, FaceTrimUser


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = get_user_model()
        fields = ['username', 'password']


class RegisterUserForm(forms.ModelForm):
    username = forms.CharField(label="Логин")
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Повтор пароля", widget=forms.PasswordInput)

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'first_name', 'last_name', 'password', 'password2']
        labels = {
            'email': 'E-mail',
            'first_name': 'Имя',
            'last_name': 'Фамилия',
        }

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError("Пароли не совпадают!")
        return cd['password2']

    def clean_email(self):
        email = self.cleaned_data['email']
        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError("Такой E-mail уже существует!")
        return email


class FeedbackForm(forms.ModelForm):
    descriptions = forms.CharField(label='Описание', widget=forms.TextInput(attrs={'class': 'form-input'}))

    class Meta:
        model = Feedback
        fields = ['descriptions', 'users_id']


class TrimmingPhotoForm(forms.ModelForm):
    class Meta:
        model = FaceTrimUser
        fields = ['face_photo', 'users_id']


class AgeGenderRaceForm(forms.Form):
    path = forms.CharField()


class UpdateDataPhotoForm(forms.Form):
    id = forms.IntegerField()
    name = forms.CharField(label="Имя")
    description = forms.CharField(label="Описание", required=False)
    age = forms.IntegerField(label="Возраст")
    dominant_gender = forms.CharField(label="Пол")
    dominant_race = forms.CharField(label="Раса")
    dominant_emotion = forms.CharField(label="Эмоция")
    users_id = forms.IntegerField(label="id пользователя")


class DeletePhotoForm(forms.Form):
    id = forms.IntegerField()
