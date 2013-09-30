from django.contrib.auth.models import User, Group
from django.forms import widgets
from rest_framework import serializers

from api.models import Page


class UserSerializer(serializers.HyperlinkedModelSerializer):
    pages = serializers.HyperlinkedRelatedField(many=True, view_name='page-detail')

    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'pages')


class PageSerializer(serializers.HyperlinkedModelSerializer):
    author = serializers.Field(source='author.username')

    class Meta:
        model = Page
        fields = ('url', 'id', 'created', 'title', 'body', 'author')
