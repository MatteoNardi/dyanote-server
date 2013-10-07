"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.core.urlresolvers import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status

from api import urls, models, serializers, views

# Costants in the example data
# Client credentials for OAuth2 authentication
USERNAME = 'user1'
PASSWORD = 'pwd'
CLIENT_ID = 'bb05c6ab017f50116084'
CLIENT_SECRET = '4063c2648cdd7f2e4dae563da80a516f2eb6ebb6'
ACCESS_TOKEN = '1b24279ad7d5986301583538804e5240c3e588af'

class SimpleTest(APITestCase):
    # Load example data
    fixtures = ['test-db.json']

    def setUp(self):
    	self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + ACCESS_TOKEN)

    def test_login(self):
        # Remove credentials
        self.client.credentials()
        params = {
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'grant_type': 'password',
            'username': USERNAME,
            'password': PASSWORD
        }
        response = self.client.post("/api/oauth2/access_token", params)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_with_wrong_password(self):
        # Remove credentials
        self.client.credentials()
        params = {
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'grant_type': 'password',
            'username': USERNAME,
            'password': PASSWORD + "..ops!"
        }
        response = self.client.post("/api/oauth2/access_token", params)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_users_list_forbidden(self):
        response = self.client.get("/api/users/{0}/".format(USERNAME))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_page_list(self):
        response = self.client.get("/api/users/{0}/pages/".format(USERNAME))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for page in response.data: del page['created'] # Do not check dates (it's hard to do well)  
        self.assertEqual(response.data, [{"url": "http://testserver/api/users/user1/pages/1/", "id": 1, "title": "Example page", "body": "Lore ipsum...", "author": "user1"}, {"url": "http://testserver/api/users/user1/pages/2/", "id": 2, "title": "Example page 2", "body": "Lorem ipsum dolorem...", "author": "user1"}])