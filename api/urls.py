from django.conf.urls import patterns, url, include
from rest_framework.urlpatterns import format_suffix_patterns

from api import views, user_views


# API endpoints
urlpatterns = format_suffix_patterns(patterns('api.views',
    url(r'^$', 'api_root'),
    url(r'^users/$',
        user_views.ListCreateUsers.as_view(),
        name='user-list'),
    url(r'^users/(?P<username>[\w@\.]+)/$',
        user_views.UserDetail.as_view(),
        name='user-detail'),
    url(r'^users/(?P<username>[\w@\.]+)/activate/$',
        user_views.activate,
        name='user-activate'),
    url(r'^users/(?P<username>[\w@\.]+)/password/$',
        user_views.UpdateResetPassword.as_view(),
        name='password'),
    url(r'^users/(?P<username>[\w@\.]+)/pages/$',
        views.PageList.as_view(),
        name='page-list'),
    url(r'^users/(?P<username>[\w@\.]+)/pages/(?P<pk>[0-9]+)/$',
        views.PageDetail.as_view(),
        name='page-detail'),
))

# Login and logout views for the browsable API
urlpatterns += patterns('',    
    url(r'^oauth2/', include('provider.oauth2.urls', namespace='oauth2')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
)
