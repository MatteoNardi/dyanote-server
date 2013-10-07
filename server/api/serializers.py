from django.contrib.auth.models import User
from django.forms import widgets
from rest_framework import serializers, relations
from rest_framework.reverse import reverse

from api.models import Page

class PageIdentityField(relations.HyperlinkedIdentityField):
    """ Hyperlinking support for our Page url scheme. """
    def get_url(self, obj, view_name, request, format):
        kwargs = {'username': obj.author.username, 'pk': obj.id}
        return reverse(view_name, kwargs=kwargs, request=request, format=format)

    def get_object(self, queryset, view_name, view_args, view_kwargs):
        username = view_kwargs['username']
        id = view_kwargs['pk']
        return queryset.get(username=account, id=id)


class UserSerializer(serializers.HyperlinkedModelSerializer):
    pages = serializers.HyperlinkedIdentityField(
        view_name='page-list', 
        lookup_field='username'
    )

    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'pages')
        lookup_field='username'


class PageSerializer(serializers.HyperlinkedModelSerializer):
    url = PageIdentityField(view_name='page-detail')
    author = serializers.Field(source='author.username')

    class Meta:
        model = Page
        fields = ('url', 'id', 'created', 'title', 'body', 'author')
