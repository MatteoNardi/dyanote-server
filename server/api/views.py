from django.contrib.auth.models import User
from rest_framework import mixins
from rest_framework import generics
from rest_framework import renderers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

from api.models import Page
from api.serializers import UserSerializer, PageSerializer



@api_view(('GET',))
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'pages': reverse('page-list', request=request, format=format)
    })


class UserList(generics.ListAPIView):
    """
    API endpoint that allows users to be listed.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class PageList(generics.ListCreateAPIView):
    """
    API endpoint that allows pages to be listed and created.
    """
    queryset = Page.objects.all()
    serializer_class = PageSerializer

    def pre_save(self, obj):
    	obj.author = self.request.user


class PageDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint that allows pages to be viewed, updated and deleted.
    """
    queryset = Page.objects.all()
    serializer_class = PageSerializer

    def pre_save(self, obj):
    	obj.author = self.request.user
