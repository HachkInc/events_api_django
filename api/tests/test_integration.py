from django.test import TestCase
from django.urls import reverse
from rest_framework import status


class IntegrationTest(TestCase):
    def setUp(self) -> None:
        self.data_register = {
            "id": "HASHID1234567890",
            "email": "user@example.com",
            "password": "pass"
        }
        self.data_auth =  {
            "username": self.data_register['email'],
            "password": self.data_register['password']
        }

    def test_auth(self):
        url_reg = '/api/v1/auth/register'
        url_auth = '/api/v1/auth/login'

        response = self.client.post(url_reg, self.data_register)
        response_auth = self.client.post(url_auth, self.data_auth)
        self.assertEqual(response_auth.status_code, status.HTTP_200_OK)
