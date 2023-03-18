import json
from datetime import datetime

import pytz
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from api.models import Events, User, Tickets
from api.serializers import EventsSerializer, UserSerializer


class EventsApiTestCase(APITestCase):
    def setUp(self) -> None:
        self.d_start = datetime(2023, 10, 9, 23, 55, 59, 342380)
        self.d_end = datetime(2023, 10, 10, 13, 55, 59, 342380)
        self.events_1 = Events.objects.create(id='test1', title="Test Event", login="Test login",
                                              password="Test-password",
                                              address="Test address",
                                              time_start=self.d_start, time_end=self.d_end, max_guest_count=100,
                                              description="Test description")
        self.events_2 = Events.objects.create(id='test2', title="Test2 Event", login="Test2login",
                                              password="Test-password2",
                                              address="Test2 address",
                                              time_start=self.d_start, time_end=self.d_end, max_guest_count=200,
                                              description="Test2 description")
        self.json_data = {
            "id": "sstring",
            "title": "string",
            "login": "string",
            "password": "string",
            "address": "string",
            "time_start": "2023-03-04T11:02:07.197Z",
            "time_end": "2023-03-04T11:02:07.197Z",
            "max_guest_count": 10,
            "description": "string"
        }
        self.event1_data = {
            'id': 'test1',
            'title': 'Test Event',
            'login': 'Test Login',
            'password': 'Test-password',
            'address': 'Test address',
            'time_start': '2023-10-09T23:55:59.342380Z',
            'time_end': '2023-10-10T13:55:59.342380Z',
            'max_guest_count': 100,
            'description': 'Test description'
        }
        self.fail_json_data = {
            'id': 'test1',
            'title': 'Test Event',
            'login': 'Test login',
            'password': 'Test-password',
            'address': 'Test address',
            'time_start': '2023-10-09T23:55:59.342380Z',
            'time_end': '2023-10-10T13:55:59.342380Z',
            # 'max_guest_count': 100,
            'description': 'Test description'
        }

    def test_get_all(self):
        url = reverse('events-list')
        response = self.client.get(url)

        serializer_data = EventsSerializer([self.events_1, self.events_2], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_get_one(self):
        url = reverse('events-detail', args=[self.events_1.id])
        response = self.client.get(url)

        serializer_data = EventsSerializer(self.events_1).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_get_one_fail(self):
        url = reverse('events-detail', args=['unknown_id'])
        response = self.client.get(url)

        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

    def test_create(self):
        url = reverse('events-list')
        response = self.client.post(url, self.json_data)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

    def test_create_fail(self):
        url = reverse('events-list')
        response = self.client.post(url, self.fail_json_data)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_update(self):
        url = reverse('events-detail', args=[self.events_1.id])
        response = self.client.put(url, self.event1_data)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(self.event1_data, response.data)

    def test_update_fail(self):
        url = reverse('events-detail', args=[self.events_1.id])
        response = self.client.put(url, self.fail_json_data)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_delete(self):
        url = reverse('events-detail', args=[self.events_1.id])
        response = self.client.delete(url)
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

    def test_delete_fail(self):
        url = reverse('events-detail', args=['unknown_test_id'])
        response = self.client.delete(url)
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)


class UsersTestCase(APITestCase):

    def setUp(self) -> None:
        self.user_1 = User.objects.create(id='test_id11', first_name='Test_first_name', last_name='Test_last_name',
                                          age=20,
                                          is_superuser=False, is_staff=False, password="test_password")
        self.expected_user_data = {
            'id': 'test_id11',
            'first_name': 'Test_first_name',
            'last_name': 'Test_last_name',
            'age': 20,
            'is_superuser': False,
            'is_staff': False,
            'username': '',
            'password': 'test_password'
        }
        self.data_to_create = {
            'id': 'test',
            'first_name': 'Test',
            'last_name': 'Test',
            'age': 20,
            'is_superuser': False,
            'is_staff': False,
            'username': 'test@test.ru',
            'password': 'test',
        }
        self.fail_data = {
            'first_name': 'Test',
        }
        self.data_to_update = {
            'id': 'test_id11',
            'first_name': 'Test_first_name',
            'last_name': 'Test_last_name',
            'age': 20,
            'is_superuser': False,
            'is_staff': False,
            'username': 'test',
            'password': 'test_password',
        }

    def test_get_all(self):
        url = reverse('user-list')
        response = self.client.get(url)

        not_expected_data = []
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertNotEqual(not_expected_data, response.data)

    def test_get_one(self):
        url = reverse('user-detail', args=[self.user_1.id])
        response = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        self.assertEqual(self.expected_user_data, response.data)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_get_one_false(self):
        url = reverse('user-detail', args=['test'])
        response = self.client.get(url)
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

    def test_create(self):
        url = reverse('user-list')
        response = self.client.post(url, self.data_to_create)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(self.data_to_create, response.data)

    def test_create_fail(self):
        url = reverse('user-list')
        response = self.client.post(url, self.fail_data)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_update(self):
        url = reverse('user-detail', args=[self.user_1.id])
        response = self.client.put(url, self.data_to_update)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(self.data_to_update, response.data)

    def test_update_fail(self):
        url = reverse('user-detail', args=['not_found_id'])
        response = self.client.put(url, self.data_to_update)
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

    def test_delete(self):
        url = reverse('user-detail', args=[self.user_1.id])
        response = self.client.delete(url)
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

    def test_delete_fail(self):
        url = reverse('user-detail', args=['unknown_id'])
        response = self.client.delete(url)
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)


class TicketsTestCase(APITestCase):
    def setUp(self) -> None:
        self.user_1 = User.objects.create(id='test_id11', first_name='Test_first_name', last_name='Test_last_name',
                                          age=20,
                                          is_superuser=False, is_staff=False, password="test_password")
        self.d_start = datetime(2023, 10, 9, 23, 55, 59, 342380, tzinfo=pytz.UTC)
        self.d_end = datetime(2023, 10, 10, 13, 55, 59, 342380, tzinfo=pytz.UTC)
        self.event_1 = Events.objects.create(id='test_event_id1', title='Test Event', login='Test login',
                                             password='Test-password',
                                             address='Test address',
                                             time_start=self.d_start, time_end=self.d_end, max_guest_count=100,
                                             description='Test description')
        self.ticket_1 = Tickets.objects.create(id='test_id1', event_id=self.event_1, user_id=self.user_1,
                                               is_inside=False)
        self.data_json = {
            'id': 'test_id2',
            'event_id': 'test_event_id1',
            'user_id': 'test_id11',
            'is_inside': False
        }
        self.invalid_data_json = {
            'id': 'test_id1',
            'event_id': 'unknown_id',
            'user_id': 'test_user_id1',
            'is_inside': False
        }
        self.data_json_update = {
            'id': 'test_id2',
            'event_id': 'test_event_id1',
            'user_id': 'test_id11',
            'is_inside': True
        }

    def test_get_all(self):
        url = reverse('tickets-list')
        response = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_get_one(self):
        url = reverse('tickets-detail', args=[self.ticket_1.id])
        response = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_get_one_fail(self):
        url = reverse('tickets-detail', args=['unknown_id'])
        response = self.client.get(url)
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

    def test_create(self):
        url = reverse('tickets-list')
        response = self.client.post(url, self.data_json)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(self.data_json, response.data)

    def test_create_fail(self):
        url = reverse('tickets-list')
        response = self.client.post(url, self.invalid_data_json)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_update(self):
        url = reverse('tickets-detail', args=[self.ticket_1.id])
        response = self.client.put(url, self.data_json_update)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(self.data_json_update, response.data)

    def test_update_fail(self):
        url = reverse('tickets-detail', args=[self.ticket_1.id])
        response = self.client.put(url, self.invalid_data_json)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_delete(self):
        url = reverse('tickets-detail', args=[self.ticket_1.id])
        response = self.client.delete(url)
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

    def test_delete_fail(self):
        url = reverse('tickets-detail', args=['unknown_id'])
        response = self.client.delete(url)
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)
