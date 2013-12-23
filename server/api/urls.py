from django.conf.urls import patterns, url, include
from rest_framework.urlpatterns import format_suffix_patterns

from api import views


# API endpoints
urlpatterns = format_suffix_patterns(patterns('api.views',
    url(r'^$', 'api_root'),
    url(r'^users/$',
        views.UserList.as_view(),
        name='user-list'),
    url(r'^users/(?P<username>.+)/$',
        views.UserDetail.as_view(),
        name='user-detail'),
    url(r'^users/(?P<username>.+)/pages/$',
        views.PageList.as_view(),
        name='page-list'),
    url(r'^users/(?P<username>.+)/pages/(?P<pk>[0-9]+)/$',
        views.PageDetail.as_view(),
        name='page-detail'),
))

# Login and logout views for the browsable API
urlpatterns += patterns('',    
    url(r'^oauth2/', include('provider.oauth2.urls', namespace='oauth2')),
)
