from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import mixins
from rest_framework import generics
from rest_framework import renderers
from rest_framework import permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

from api.models import Page
from api.serializers import UserSerializer, SimplePageSerializer, FullPageSerializer
from api.permissions import IsOwnerOrAdmin


@api_view(('GET',))
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
    })


class UserList(generics.ListAPIView):
    """
    API endpoint that allows users to be listed.
    """
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return User.objects.all()
        return [user,]

class UserDetail(generics.RetrieveAPIView):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrAdmin)

    def get_object(self):
        return get_object_or_404(User, username=self.kwargs['username'])


class PageList(generics.ListCreateAPIView):
    """
    API endpoint that allows pages to be listed and created.
    """
    serializer_class = SimplePageSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrAdmin)

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Page.objects.all()
        return Page.objects.filter(author=user)

    def pre_save(self, obj):
    	obj.author = self.request.user


class PageDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint that allows pages to be viewed, updated and deleted.
    """
    serializer_class = FullPageSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrAdmin)

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Page.objects.all()
        return Page.objects.filter(author=user)

    def pre_save(self, obj):
    	obj.author = self.request.user
