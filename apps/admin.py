from django.contrib import admin
from django.contrib.auth.models import User

from .models import CrimeReport, Profile, Notification
from .forms import NotificationForm

# Register your models here.

admin.site.register(CrimeReport)
admin.site.register(Profile)


class NotificationAdmin(admin.ModelAdmin):
    form = NotificationForm
    list_display = ['user', 'content', 'read', 'timestamp']

    def save_model(self, request, obj, form, change):
        select_all_users = form.cleaned_data.get('select_all_users')
        if select_all_users:
            users = User.objects.all()
            notifications = [Notification(user=user, content=form.cleaned_data.get('content')) for user in users]
            Notification.objects.bulk_create(notifications)
        else:
            super().save_model(request, obj, form, change)


admin.site.register(Notification, NotificationAdmin)
