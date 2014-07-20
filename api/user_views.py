import hashlib
import random

from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.template.loader import render_to_string

from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework import exceptions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from api.permissions import IsOwnerOrAdmin
from api.serializers import UserSerializer, NewUserSerializer, PasswordSerializer
from api.models import ActivationKey
from api.utils import mail_user

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
        mail_user(user, 'Welcome to Dyanote', 
            'api/activation_email.txt', key=activation_key.key)

        return Response(serialized.data, status=status.HTTP_201_CREATED)


def create_activation_key(user):
    salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
    email = user.email
    if isinstance(email, unicode):
        email = email.encode('utf-8')
    activation_key = hashlib.sha1(salt+email).hexdigest()
    return ActivationKey.objects.create(user=user, key=activation_key)


@api_view(('GET',))
def activate(request, username):
    """ Activate a user after registration """
    email = self.kwargs.get('username', '')
    key = request.QUERY_PARAMS.get('key', '')
    try:
        activation_key = ActivationKey.objects.get(user=email, key=key)
        activation_key.user.is_active = True
        activation_key.user.save()
        activation_key.delete()
        tpl = render_to_string('api/activation_succeeded.html', user=email)
        return Response(tpl, status=status.HTTP_200_OK)
    except ActivationKey.DoesNotExist:
        redirect('https://dyanote.com')


class UpdateResetPassword(APIView):
    def put(self, request, format=None):
        """ Change password """
        if not request.successful_authenticator:
            raise exceptions.NotAuthenticated()

        if request.user.email != self.kwargs.get('email'):
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        password = PasswordSerializer(data=request.DATA)
        if not password.is_valid():
            return Response(password._errors, status=status.HTTP_400_BAD_REQUEST)

        if not request.user.check_password(password.old):
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)

        request.user.set_password(password.new)
        request.user.save()

    def delete(self, request, format=None):
        """ Reset password """
        try:
            user = User.objects.get(email=kwargs['email'])
            password = User.objects.make_random_password()
            user.set_password(password)
            user.save()
            mail_user(user, 'New Dyanote password',
                'api/new_password.txt', password=password)

        except User.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST) 

# TODO: Create a login view which checks the username specified in the url is the same as
# the username in the params.