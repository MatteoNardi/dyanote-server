"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.core.urlresolvers import reverse
from rest_framework.test import APITestCase, APIClient


from api import urls, models, serializers, views

class SimpleTest(APITestCase):
    fixtures = ['test-db.json']

    def setUp(self):
    	self.client = APIClient()

    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)
