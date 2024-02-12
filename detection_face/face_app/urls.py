from django.contrib.auth.views import LogoutView
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.LoginUser.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('registration/', views.registration, name='registration'),
    path('working_with_images/<int:users_id>/', views.working_with_images, name='working_with_images'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
