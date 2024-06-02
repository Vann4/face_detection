from django.contrib import admin
from django.contrib.auth.models import Group
from .models import Feedback


class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('name', 'descriptions', 'email')
    search_fields = ('name', 'email')
    list_filter = ('email',)


admin.site.register(Feedback, FeedbackAdmin)
admin.site.unregister(Group)