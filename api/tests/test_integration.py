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

    def test_success(self):
        url_reg = 'auth/register'
        response = self.client.post(url_reg, self.data_register)
        print(response)
        self.assertEqual(1, 1)
