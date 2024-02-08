from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, FaceTrimUser, Feedback


admin.site.register(User, UserAdmin)
admin.site.register(FaceTrimUser)
admin.site.register(Feedback)
