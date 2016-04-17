from django.conf.urls import patterns, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^edit/', 't5_edit.views.edit', name='edit'),
)
