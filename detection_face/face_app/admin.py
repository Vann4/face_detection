from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from .models import User, Feedback


admin.site.register(User, UserAdmin)
admin.site.register(Feedback)
admin.site.unregister(Group)
