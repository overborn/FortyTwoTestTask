from django.conf.urls import patterns, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^edit/', 't5_edit.views.edit', name='edit'),
    url(r'^ajax_save/', 't5_edit.views.ajax_save', name='ajax_save'),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login',
        name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout',
        {'next_page': '/'}, name='logout')
)
