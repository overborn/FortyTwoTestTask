from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    # Examples:
    # url(r'^$', 'fortytwo_test_task.views.home', name='home'),
    url("", include('t1_contact.urls')),
    url("", include('t3_requests.urls')),
    url("", include('t5_edit.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
