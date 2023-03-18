import json
from collections import OrderedDict
from datetime import datetime

import pytz
from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from api.models import User, Events, Tickets


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
            'email': 'user@example.com',
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

        self.data_to_update = {
            "id": "HASHID1234567890",
            "first_name": "string",
            "last_name": "string",
            "age": 1,
            "is_superuser": True,
            "is_staff": True,
            "username": "string123123",
            "password": "string123123"
        }

        self.data_ticket_invalid_update = {
            'id': 'test_id',
            'event_id': 'test_event_id1',
            'user_id': 'test_id11',
            'is_inside': 2134
        }


        self.data_register2 = {
            "id": "HASHID1234567dqwr1234890",
            "email": "usedasdr@example.com",
            "password": "pa11ss"
        }
        self.event_data2 = {
            "id": "string1241",
            "title": "Bamboo",
            "login": "string",
            "password": "string",
            "address": "string",
            "time_start": "2023-03-17T23:12:45.715Z",
            "time_end": "2023-03-17T23:12:45.715Z",
            "max_guest_count": 10,
            "description": "string"
        }

        self.user_1 = User.objects.create(id='HASHID1234567dqwr1234890', first_name='Test_first_name', last_name='Test_last_name',
                                          age=20,
                                          is_superuser=False, is_staff=False, password="test_password")
        self.d_start = datetime(2023, 10, 9, 23, 55, 59, 342380, tzinfo=pytz.UTC)
        self.d_end = datetime(2023, 10, 10, 13, 55, 59, 342380, tzinfo=pytz.UTC)
        self.event_1 = Events.objects.create(id='string1241', title='Test Event', login='Test login',
                                             password='Test-password',
                                             address='Test address',
                                             time_start=self.d_start, time_end=self.d_end, max_guest_count=100,
                                             description='Test description')
        self.data_ticket_valid = {
            'id': 'test_id',
            'event_id': 'string1241',
            'user_id': 'HASHID1234567dqwr1234890',
            'is_inside': False
        }


        self.data_ticket_invalid = {
            'id': 'test_id',
            'event_id': 'not_exist_event',
            'user_id': 'not_exist_user',
            'is_inside': False
        }


    def test_register(self):
        url_reg = '/api/v1/auth/register'
        url_auth = '/api/v1/auth/login'

        response = self.client.post(url_reg, self.data_register)
        response_auth = self.client.post(url_auth, self.data_auth)
        self.assertEqual(response_auth.status_code, status.HTTP_200_OK)

    def test_fail_register(self):
        url_reg = '/api/v1/auth/register'
        response_reg1 = self.client.post(url_reg, self.data_register) # здесь исправь новый словарь создай

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


    def test_create_ticket_success(self):
        url = '/api/v1/tickets/'
        response = self.client.post(url, data=json.dumps(self.data_ticket_valid), content_type="application/json")
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(self.data_ticket_valid, response.data)

    def test_create_ticket_fail(self):
        url = '/api/v1/tickets/'
        response = self.client.post(url, data=json.dumps(self.data_ticket_invalid), content_type="application/json")
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
