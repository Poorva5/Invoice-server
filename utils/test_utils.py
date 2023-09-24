from django.test import TestCase
from rest_framework.test import APIClient

class APITest(TestCase):
    """Base API Test Class"""

    def setUp(self):
        """Will setup base for tests"""
        super().setUp()
        self.client = APIClient()

