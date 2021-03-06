from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.core.mail import send_mail
from django.shortcuts import redirect, get_object_or_404
from django.template.loader import render_to_string
from django.http import HttpResponse as DjangoResponse
from django.views.decorators.csrf import csrf_exempt

from oauth2_provider.views.base import TokenView

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
from api import utils
from api.utils import mail_user, user_exists, generate_activation_key, get_client_url

class UserDetail(generics.RetrieveAPIView):
    """
    API endpoint that allows users to be viewed.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrAdmin)

    def get_object(self):
        return get_object_or_404(User, username=self.kwargs['username'])


class ListCreateUsers(APIView):
    def get(self, request, format=None):
        """
        Get the list of users you can access (either all users if you're admin
        or just yourself if you're a normal user) 
        """
        if not request.successful_authenticator:
            raise exceptions.NotAuthenticated()
        user = self.request.user
        dataset = User.objects.all() if user.is_superuser else [user,]
        serializer = UserSerializer(dataset, many=True, 
                                    context={'request': request})
        return Response(serializer.data)

    def post(self, request, format=None):
        """
        Register a new user 
        """
        serialized = NewUserSerializer(data=request.DATA)
        if not serialized.is_valid():
            return Response(serialized._errors, status=status.HTTP_400_BAD_REQUEST)

        email = serialized.initial_data['email']
        pwd = serialized.initial_data['password']

        user = None
        if User.objects.filter(email=email).count():
            user = User.objects.get(email=email)
            if user.is_active:
                return Response(status=status.HTTP_409_CONFLICT)
            # If an inactive user already exists, change passsword and send
            # a new activation mail
            user.set_password(pwd)
        else:
            # Create user
            username = email
            user = User.objects.create_user(username, email, pwd)
            user.is_active = False
        user.save()

        key = generate_activation_key(user)
        activation_key = None
        # If user has already an activation key, replace it.
        if ActivationKey.objects.filter(user=user).count():
            activation_key = ActivationKey.objects.get(user=user)
            activation_key.key = key
            activation_key.save()
        else:
            activation_key = ActivationKey.objects.create(user=user, key=key)

        utils.mail_user(user, 'Welcome to Dyanote', 
            'api/activation_email.txt', key=activation_key.key)

        return Response(serialized.data, status=status.HTTP_201_CREATED)


@api_view(('GET',))
def activate(request, username, **kwargs):
    """ Activate a user after registration """
    key = request.QUERY_PARAMS.get('key', '')
    try:
        # Create activation keys
        activation_key = ActivationKey.objects.get(key=key, user__username=username)
        activation_key.user.is_active = True
        activation_key.user.save()
        activation_key.delete()
        # Create default notes
        utils.setup_default_notes(activation_key.user)
        tpl = render_to_string('api/activation_succeeded.html', { 'user': username })
        return DjangoResponse(tpl, status=status.HTTP_200_OK)
    except ActivationKey.DoesNotExist:
        return redirect(get_client_url())


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
            utils.mail_user(user, 'New Dyanote password',
                'api/new_password.txt', password=password)

        except User.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST) 


class Login(TokenView):

    def post(self, request, username):
        if user_exists(username):
            user = User.objects.get(username=username)
            # Check if user is active
            if user.is_active is False:
                return DjangoResponse('User is not active',
                                      status=status.HTTP_401_UNAUTHORIZED)
        # Check if the username in parameters metches the username in url
        # print("\npath username: {}".format(username))
        # print("\nparam username: {}".format(request.POST.get('username')))
        if username != request.POST.get('username'):
            # print('\nfail\n')
            return DjangoResponse('Mismatching usernames',
                                  status=status.HTTP_401_UNAUTHORIZED)
        return super().post(request)
