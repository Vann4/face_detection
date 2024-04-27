from django.contrib.auth.views import LogoutView, PasswordChangeView, PasswordChangeDoneView
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.LoginUser.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('registration/', views.registration, name='registration'),
    path('user_profile/', views.UserProfile.as_view(), name='user_profile'),
    path('password-change/', views.UserPasswordChange.as_view(), name="password_change"),
    path('password-change/done/', PasswordChangeDoneView.as_view(template_name="face_app/password_change_done.html"), name="password_change_done"),
    path('working_with_images/<int:users_id>/', views.working_with_images, name='working_with_images'),
    path('live_feed/<int:users_id>/', views.live_feed, name='live_feed'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
