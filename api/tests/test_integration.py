from collections import OrderedDict

from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from api.models import User


class IntegrationTest(TestCase):
    def setUp(self) -> None:
        self.data_register = {
            "id": "HASHID1234567890",
            "email": "user@example.com",
            "password": "pass"
        }
        self.data_register2 = {
            'id': 'SOMERANDOMID141241',
            'email': 'exist_str@mail.ru',
            'password': 'test_password'
        }

        self.data_auth = {
            "username": self.data_register['email'],
            "password": self.data_register['password']
        }

        self.data_register_false = {
            "id": "random_id123",
            'email': 'exist_str@mail.ru',
            "password": "somepassword"
        }

        self.data_auth_fail = {
            'username': 'dasfafaf',
            'password': 'test_password'
        }
        self.event_data = {
            "id": "string",
            "title": "string",
            "login": "string",
            "password": "string",
            "address": "string",
            "time_start": "2023-03-17T23:12:45.715Z",
            "time_end": "2023-03-17T23:12:45.715Z",
            "max_guest_count": 0,
            "description": "string"
        }
        self.fail_event_data = {
            'id': 'test1',
            'title': 'Test Event',
            'login': 'Test login',
            'password': 'Test-password',
            # 'address': 'Test address',
            'time_start': '2023-10-09T23:55:59.342380Z',
            'time_end': '2023-10-10T13:55:59.342380Z',
            'max_guest_count': 100,
            'description': 'Test description'
        }

    def test_register(self):
        url_reg = '/api/v1/auth/register'
        url_auth = '/api/v1/auth/login'

        response = self.client.post(url_reg, self.data_register)
        response_auth = self.client.post(url_auth, self.data_auth)
        self.assertEqual(response_auth.status_code, status.HTTP_200_OK)

    def test_fail_register(self):
        url_reg = '/api/v1/auth/register'
        response_reg1 = self.client.post(url_reg, self.data_register2)

        response_reg_fail = self.client.post(url_reg, self.data_register_false)

        self.assertIn("This field must be unique.", response_reg_fail.data['email'])
        self.assertEqual(response_reg_fail.status_code, status.HTTP_400_BAD_REQUEST)

    def test_fail_auth(self):
        url_auth = '/api/v1/auth/login'
        response = self.client.post(url_auth, self.data_auth_fail)
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("No active account found with the given credentials", response.data['detail'])

    def test_create_event(self):
        url_event = '/api/v1/events/'
        find_event = url_event + "?word=string"
        response = self.client.post(url_event, self.event_data)
        response_get = self.client.get(find_event)

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(list(response_get.data[0]), list(OrderedDict(self.event_data)))

    def test_create_event_fail(self):
        url_event = '/api/v1/events/'
        response = self.client.post(url_event, self.fail_event_data)

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)



    def test_fake(self):
        self.assertEqual(1, 1)
