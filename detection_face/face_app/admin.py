from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from .models import User, Feedback

admin.site.register(User, UserAdmin)


class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('name', 'descriptions', 'email')
    search_fields = ('name', 'email')
    list_filter = ('email',)


admin.site.register(Feedback, FeedbackAdmin)
admin.site.unregister(Group)
