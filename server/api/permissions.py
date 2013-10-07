from django.contrib.auth.models import User
from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit and view it.
    """
    def has_object_permission(self, request, view, obj):
        return obj.author == request.user

    def has_permission(self, request, view):
        try:
            user = User.objects.get(username=view.kwargs['username'])
        except User.DoesNotExist:
            return False
        
        return user == request.user

