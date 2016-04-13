from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    # Examples:
    # url(r'^$', 'fortytwo_test_task.views.home', name='home'),
    url(r'^$', 't1_contact.views.index', name='index'),
    url(r'^t1/', include('t1_contact.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
