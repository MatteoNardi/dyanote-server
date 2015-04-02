from django.contrib.auth.models import User
from django.forms import widgets
from rest_framework import serializers, relations
from rest_framework.reverse import reverse

from api.models import Page

class PageIdentityField(relations.HyperlinkedIdentityField):
    """ Hyperlinking support for our Page url scheme. """
    def get_url(self, obj, view_name, request, format):
        kwargs = {'username': obj.author.username, 'pk': obj.pk}
        return reverse(view_name, kwargs=kwargs, request=request, format=format)

    def get_object(self, view_name, view_args, view_kwargs):
        return Page.objects.get(pk=view_kwargs['pk'])

    def use_pk_only_optimization(self):
        return False;

class PageRelatedField(relations.HyperlinkedRelatedField):
    """ Hyperlinking support for our Page url scheme. """
    def get_url(self, obj, view_name, request, format):
        kwargs = {'username': obj.author.username, 'pk': obj.pk}
        return reverse(view_name, kwargs=kwargs, request=request, format=format)

    def get_object(self, view_name, view_args, view_kwargs):
        return Page.objects.get(pk=view_kwargs['pk'])

    def use_pk_only_optimization(self):
        return False;


class NewUserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=100)

class UserSerializer(serializers.HyperlinkedModelSerializer):
    pages = serializers.HyperlinkedIdentityField(
        view_name='page-list', 
        lookup_field='username'
    )

    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'pages')
        lookup_field='username'

class PasswordSerializer(serializers.Serializer):
    old = serializers.CharField(max_length=100)
    new = serializers.CharField(max_length=100)

class PageSerializer(serializers.HyperlinkedModelSerializer):
    url = PageIdentityField(view_name='page-detail')
    author = serializers.HyperlinkedRelatedField(view_name='user-detail', read_only=True,
                                                 lookup_field='username')
    parent = PageRelatedField(view_name='page-detail', required=False, queryset=Page.objects.all())
    flags = serializers.SerializerMethodField()

    class Meta:
        model = Page
        fields = ('url', 'id', 'parent', 'created', 'title', 'body', 'author', 'flags')

    def get_flags(self, obj):
        return {
            Page.NORMAL: [],
            Page.ROOT: ['root'],
            Page.ARCHIVE: ['archive'],
        }[obj.flags]

