import hashlib
import random

from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.template.loader import render_to_string

from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.permissions import IsOwnerOrAdmin
from api.serializers import UserSerializer, PageSerializer, NewUserSerializer
from api.models import ActivationKey

class UserDetail(generics.RetrieveAPIView):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrAdmin)

    def get_object(self):
        return get_object_or_404(User, username=self.kwargs['username'])


class ListCreateUsers(APIView):
    def get(self, request, format=None):
        """
        Get the list of users you can edit (either all users if you're admin
        or just yourself if you're a normal user) 
        """
        if not request.successful_authenticator:
            raise exceptions.NotAuthenticated()
        user = self.request.user
        dataset = User.objects.all() if user.is_superuser else [user,]
        serializer = UserSerializer(dataset, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        """
        Register a new user 
        """
        serialized = NewUserSerializer(data=request.DATA)
        if not serialized.is_valid():
            return Response(serialized._errors, status=status.HTTP_400_BAD_REQUEST)

        email = serialized.init_data['email']
        pwd = serialized.init_data['password']
        # If user already exists, return 409
        if User.objects.filter(email=email).count():
            return Response(status=status.HTTP_409_CONFLICT)
        
        # Create user
        user = User.objects.create_user(email, email, pwd)
        user.is_active = False
        user.save()
        activation_key = create_activation_key(user)
        send_activation_mail(user, activation_key)

        return Response(serialized.data, status=status.HTTP_201_CREATED)


def create_activation_key(user):
    salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
    email = user.email
    if isinstance(email, unicode):
        email = email.encode('utf-8')
    activation_key = hashlib.sha1(salt+email).hexdigest()
    return ActivationKey.objects.create(user=user, key=activation_key)


def send_activation_mail(user, activation_key):
    msg = render_to_string('api/activation_email.txt', {"activation_key": activation_key.key})
    send_mail('Welcome to Dyanote', msg, 'Dyanote founder', [user.email])


