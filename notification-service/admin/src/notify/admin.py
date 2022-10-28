from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin

from .models import TemplatesNotify, Senders, TemplatesBody, Notifications


@admin.register(TemplatesBody)
class TemplatesBodyModelAdmin(SummernoteModelAdmin):
    """Template admin."""
    summernote_fields = ('content',)


@admin.register(Senders)
class SendersModelAdmin(admin.ModelAdmin):
    """Message Senders"""


@admin.register(TemplatesNotify)
class TemplatesNotifyModelAdmin(admin.ModelAdmin):
    """Message TemplatesNotify"""


@admin.register(Notifications)
class NotificationsModelAdmin(admin.ModelAdmin):
    """Message Notifications"""

    exclude = ('status',)
