from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Enable admin
    url(r'^admin/', include(admin.site.urls)),

    # Enable the application providing the REST API
    url(r'^api/', include('api.urls')),
)
