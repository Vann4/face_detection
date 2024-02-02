from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Data_user, Feedback


admin.site.register(User, UserAdmin)
admin.site.register(Data_user)
admin.site.register(Feedback)
