"""
This file contains unittests for the api app.

Use test_settings when running this:
./manage.py test --settings=dyanote.test_settings api
This will use sqlite and other settings to make test execution faster.

Command used to create test database.
./manage.py dumpdata --n --indent=4
    --natural
    -e admin
    -e sessions
    -e contenttypes
    -e auth.Permission
    -e south.migrationhistory > api/fixtures/test-db.json

To see test coverage use:
coverage run ./manage.py test --settings=dyanote.test_settings api
coverage report -m --include=api/*
coverage html
"""

from urllib import quote
import unittest
from json import loads as load_json

from django.core.urlresolvers import reverse
from django.test import TestCase
from django.contrib.auth.models import User
from django.core import mail
from django.core.exceptions import ValidationError
from rest_framework.test import APITestCase, APIClient
from rest_framework import status

from api.models import Page


# Costant values found in the test database fixture
USERNAME = 'test@dyanote.com'
PASSWORD = 'pwd'
CLIENT_ID = 'bb05c6ab017f50116084'
CLIENT_SECRET = '4063c2648cdd7f2e4dae563da80a516f2eb6ebb6'
ACCESS_TOKEN = '1b24279ad7d5986301583538804e5240c3e588af'
ADMIN_USERNAME = 'admin' 
ADMIN_PASSWORD = 'admin'


# Model test
class PageTest(APITestCase):
    fixtures = ['test-db.json']  # Load test db

    def create_page(self, author, title="Test note", parent=None, 
                    body="Lorem ipsum dol...", flags=Page.NORMAL):
        return Page.objects.create(
            author=author,
            title=title,
            parent=parent,
            body=body,
            flags=flags)

    def test_page_creation(self):
        note = self.create_page(
            author=User.objects.get(username=USERNAME),
            title="Root page",
            flags=Page.ROOT)
        self.assertTrue(isinstance(note, Page))
        note.clean()
        self.assertEqual(note.title, "Root page")

    def test_normal_page_with_no_parent_throws_error(self):
        note = self.create_page(
            author=User.objects.get(username=USERNAME),
            flags=Page.NORMAL)
        self.assertRaises(ValidationError, note.clean)


# User testing
class UserAPITest(APITestCase):
    fixtures = ['test-db.json']

    def set_token(self, token):
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token)

    def login(self, username, password):
        params = {
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'grant_type': 'password',
            'username': username,
            'password': password
        }
        path = quote('/api/users/{}/login/'.format(username))
        response = self.client.post(path, params)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token = load_json(response.content)['access_token']
        self.set_token(token)

    def test_login(self):
        params = {
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'grant_type': 'password',
            'username': USERNAME,
            'password': PASSWORD
        }
        path = quote('/api/users/{}/login/'.format(USERNAME))
        response = self.client.post(path, params)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_with_wrong_password(self):
        params = {
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'grant_type': 'password',
            'username': USERNAME,
            'password': PASSWORD + '..ops!'
        }
        path = quote('/api/users/{}/login/'.format(USERNAME))
        response = self.client.post(path, params)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_with_inactive_user(self):
        u = User.objects.create_user('test@test.com', 'test@test.com', 'pwd')
        u.is_active = False
        u.save()
        params = {
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'grant_type': 'password',
            'username': 'test@test.com',
            'password': 'pwd'
        }
        path = quote('/api/users/{}/login/'.format('test@test.com'))
        response = self.client.post(path, params)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.content, 'User is not active')

    def test_login_with_wrong_path(self):
        params = {
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'grant_type': 'password',
            'username': USERNAME,
            'password': PASSWORD
        }
        path = quote('/api/users/{}/login/'.format('wrongEmail@test.com'))
        response = self.client.post(path, params)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.content, 'Mismatching usernames')

    def test_get_user_detail_as_unauthenticated(self):
        path = quote('/api/users/{}/'.format(USERNAME))
        response = self.client.get(path)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        ERROR = '{"detail": "Authentication credentials were not provided."}'
        self.assertEqual(response.content, ERROR)

    def test_get_user_detail(self):
        self.set_token(ACCESS_TOKEN)
        path = quote('/api/users/{}/'.format(USERNAME))
        response = self.client.get(path)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        RES = ('{"url": "http://testserver/api/users/test@dyanote.com/",'
               ' "username": "test@dyanote.com", "email": "test@dyanote.com",'
               ' "pages": "http://testserver/api/users/test@dyanote.com/pages/"}')
        self.assertEqual(response.content, RES)

    def test_get_user_detail_as_admin(self):
        self.login('admin', 'admin')
        path = quote('/api/users/{}/'.format(USERNAME))
        response = self.client.get(path)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        RES = ('{"url": "http://testserver/api/users/test@dyanote.com/",'
               ' "username": "test@dyanote.com", "email": "test@dyanote.com",'
               ' "pages": "http://testserver/api/users/test@dyanote.com/pages/"}')
        self.assertEqual(response.content, RES)

    def test_get_user_list_as_unauthenticated(self):
        response = self.client.get('/api/users/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        ERROR = '{"detail": "Authentication credentials were not provided."}'
        self.assertEqual(response.content, ERROR)

    def test_get_user_list(self):
        self.set_token(ACCESS_TOKEN)
        response = self.client.get('/api/users/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        MSG = ('[{"url": "http://testserver/api/users/test@dyanote.com/",'
                ' "username": "test@dyanote.com",'
                ' "email": "test@dyanote.com",'
                ' "pages": "http://testserver/api/users/test@dyanote.com/pages/"}]')
        self.assertEqual(response.content, MSG)

    def test_user_creation(self):
        params = {
            'email': 'new_user@dyanote.com',
            'password': '123'
        } 
        response = self.client.post('/api/users/', params, format='json')

        # check mail
        msg = ("Welcome to Dyanote, your personal hypertext\.\n"
               "To activate your account, follow this link:\n"
               "https://example\.com/api/users/new_user@dyanote\.com/activate/"
               "\?key=([0-9a-fA-F]+)\n\n")
        self.assertEquals(len(mail.outbox), 1)
        self.assertEquals(mail.outbox[0].subject, 'Welcome to Dyanote')
        self.assertEquals(mail.outbox[0].from_email, 'Dyanote')
        self.assertEquals(mail.outbox[0].to, ['new_user@dyanote.com'])
        self.assertRegexpMatches(mail.outbox[0].body, msg)
        
        # check response
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

    def test_user_creation_with_invalid_data(self):
        params = {
            'email': 'new_user@dyanote.com',
        } 
        response = self.client.post('/api/users/', params, format='json')
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_recreation(self):
        params = {
            'email': USERNAME,
            'password': '123'
        } 
        response = self.client.post('/api/users/', params, format='json')
        self.assertEquals(response.status_code, status.HTTP_409_CONFLICT)




