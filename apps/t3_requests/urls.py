from django.conf.urls import patterns, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^requests/', 't3_requests.views.requests', name='requests'),
    url(r'^ajax_requests/', 't3_requests.views.ajax_requests',
        name='ajax_requests'),
)
