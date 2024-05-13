from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm

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
            'email': 'Е-мейл',
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
            raise forms.ValidationError("Такой Е-мейл уже существует!")
        return email


class FeedbackForm(forms.ModelForm):
    name = forms.CharField(label='Имя')
    descriptions = forms.CharField(label='Описание')
    email = forms.CharField(label='Е-мейл', widget=forms.TextInput(attrs={'class': 'form-input'}))

    class Meta:
        model = Feedback
        fields = ['name', 'descriptions', 'email']


class TrimmingPhotoForm(forms.ModelForm):
    class Meta:
        model = FaceTrimUser
        fields = ['face_photo', 'users_id']


class AgeGenderRaceForm(forms.Form):
    path = forms.CharField()


class UpdateDataPhotoForm(forms.Form):
    id_photo = forms.IntegerField()
    name = forms.CharField(label="Имя")
    description = forms.CharField(label="Описание", required=False)
    age = forms.IntegerField(label="Возраст", required=False)
    dominant_gender = forms.CharField(label="Пол")
    dominant_race = forms.CharField(label="Раса")
    dominant_emotion = forms.CharField(label="Эмоция")


class DeletePhotoForm(forms.Form):
    id = forms.IntegerField()


class FilterForDataOutputForm(forms.Form):
    name_filter = forms.CharField(label="Имя", required=False)
    description_filter = forms.CharField(label="Описание", required=False)
    age_filter = forms.IntegerField(label="Возраст", required=False)
    dominant_gender_filter = forms.CharField(label="Пол", required=False)
    dominant_race_filter = forms.CharField(label="Раса", required=False)
    dominant_emotion_filter = forms.CharField(label="Эмоция", required=False)
    download_date_filter = forms.DateField(label="Дата загрузки", required=False)


class UserProfileForm(forms.ModelForm):
    username = forms.CharField(disabled=True, label="Логин", widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.CharField(disabled=True, label="Е-мейл", widget=forms.TextInput(attrs={'class': 'form-input'}))

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'last_name', 'first_name']
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-input', 'required': True}),
            'last_name': forms.TextInput(attrs={'class': 'form-input', 'required': True}),
        }


class UserPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label="Старый пароль", widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    new_password1 = forms.CharField(label="Новый пароль", widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    new_password2 = forms.CharField(label="Подтверждение пароля", widget=forms.PasswordInput(attrs={'class': 'form-input'}))
