from django.contrib.auth.views import LogoutView
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # path('date_user/<int:user_id>/', views.date_user, name='date_user'),
    path('login/', views.LoginUser.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('registration/', views.registration, name='registration'),
    path('upload_face/', views.upload_face, name='upload_face'),
]
