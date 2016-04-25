from django.contrib import admin
from t3_requests.models import Request


class RequestAdmin(admin.ModelAdmin):
    list_display = (
        'method', 'priority', 'created', 'path', 'query', 'user')
    search_fields = ('method', 'created', 'path', 'query', 'user')

admin.site.register(Request, RequestAdmin)
