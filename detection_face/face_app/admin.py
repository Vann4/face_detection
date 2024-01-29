from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from face_app.models import User, Data_user


admin.site.register(User, UserAdmin)
admin.site.register(Data_user)
