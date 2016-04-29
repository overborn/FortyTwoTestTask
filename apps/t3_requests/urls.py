from django.conf.urls import patterns, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^requests/', 't3_requests.views.requests', name='requests'),
    url(r'^change_priority/', 't3_requests.views.change_priority',
        name='change_priority'),
)
