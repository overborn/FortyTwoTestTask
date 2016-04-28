from django.contrib import admin
from django.contrib.admin.models import LogEntry


class LogEntryAdmin(admin.ModelAdmin):
    list_display = [
        'action_time',
        'user',
        'content_type',
        'action_flag',
        'change_message',
    ]

admin.site.register(LogEntry, LogEntryAdmin)
