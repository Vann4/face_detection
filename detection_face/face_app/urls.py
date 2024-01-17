from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('date_user/<int:user_id>/', views.date_user, name='date_user'),
]
