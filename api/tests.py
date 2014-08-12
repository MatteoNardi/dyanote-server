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

from django.core.urlresolvers import reverse
from django.test import TestCase
from django.contrib.auth.models import User
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

    def test_login(self):
        params = {
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'grant_type': 'password',
            'username': USERNAME,
            'password': PASSWORD
        }
        path = quote("/api/users/{}/login/".format(USERNAME))
        response = self.client.post(path, params)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_with_wrong_password(self):
        params = {
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'grant_type': 'password',
            'username': USERNAME,
            'password': PASSWORD + "..ops!"
        }
        path = quote("/api/users/{}/login/".format(USERNAME))
        response = self.client.post(path, params)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_with_inactive_user(self):
        u = User.objects.create_user("test@test.com", "test@test.com", "pwd")
        u.is_active = False
        u.save()
        params = {
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'grant_type': 'password',
            'username': "test@test.com",
            'password': "pwd"
        }
        path = quote("/api/users/{}/login/".format("test@test.com"))
        response = self.client.post(path, params)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.content, "User is not active")

    def test_login_with_wrong_path(self):
        params = {
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'grant_type': 'password',
            'username': USERNAME,
            'password': PASSWORD
        }
        path = quote("/api/users/{}/login/".format("wrongEmail@test.com"))
        response = self.client.post(path, params)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.content, "Mismatching usernames")

    # def setUp(self):
    #   self.client = APIClient()
    #     self.client.credentials(HTTP_AUTHORIZATION="Bearer " + ACCESS_TOKEN)


    # def test_get_users_list_forbidden(self):
    #     response = self.client.get("/api/users/{0}/".format(USERNAME))
    #     self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # def test_get_page_list(self):
    #     response = self.client.get("/api/users/{0}/pages/".format(USERNAME))
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     for page in response.data: del page['created'] # Do not check dates (it's hard to do well)  
    #     self.assertEqual(response.data, [{"url": "http://testserver/api/users/user1/pages/1/", "id": 1, "title": "Example page", "body": "Lore ipsum...", "author": "user1"}, {"url": "http://testserver/api/users/user1/pages/2/", "id": 2, "title": "Example page 2", "body": "Lorem ipsum dolorem...", "author": "user1"}])