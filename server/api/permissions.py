from django.contrib.auth.models import User
from rest_framework import permissions


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Custom permission (For User or Page) to only allow owners of an object and admin to edit and view it.
    """
    def has_object_permission(self, request, view, obj):
        return request.user.is_superuser or obj == request.user or obj.author == request.user or request.user.is_superuser

    def has_permission(self, request, view):
        try:
            user = User.objects.get(username=view.kwargs['username'])
        except User.DoesNotExist:
            return False
        
        return request.user.is_superuser or user == request.user
