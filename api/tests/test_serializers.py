from datetime import datetime

import pytz
from django.test import TestCase

from api.models import Events, User, Tickets
from api.serializers import EventsSerializer, UserSerializer, TicketsSerializer, RegisterSerializer
from api.views import EventFilterSet


class EventsSerializerTestCase(TestCase):

    def setUp(self) -> None:
        self.d_start = datetime(2023, 10, 9, 23, 55, 59, 342380, tzinfo=pytz.UTC)
        self.d_end = datetime(2023, 10, 10, 13, 55, 59, 342380, tzinfo=pytz.UTC)
        self.event_1 = Events.objects.create(id='test_id1', title='Test Event', login='Test login',
                                             password='Test-password',
                                             address='Test address',
                                             time_start=self.d_start, time_end=self.d_end, max_guest_count=100,
                                             description='Test description')

        self.data = EventsSerializer(self.event_1).data

        self.expected_data = {
            'id': 'test_id1',
            'title': 'Test Event',
            'login': 'Test login',
            'password': 'Test-password',
            'address': 'Test address',
            'time_start': '2023-10-09T23:55:59.342380Z',
            'time_end': '2023-10-10T13:55:59.342380Z',
            'max_guest_count': 100,
            'description': 'Test description'
        }

        self.invalid_data = {
            'id': 'test_id1',
            'title': 'Test Event',
            'login': 'Test login',
            'password': 'Test-password',
            'address': 'Test address',
            'time_start': 'afmaklfjgi2ogj902',
            'time_end': 'AaaAAAAAAAAAAAAAAAAAAAAAAAAAAA',
            'max_guest_count': 100,
            'description': 'Test description'
        }

    def test_success(self):
        self.assertEqual(self.expected_data, self.data)

    def test_fail(self):
        serializer = EventsSerializer(data=self.invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('time_start', serializer.errors)
        self.assertIn('time_end', serializer.errors)


class UserSerializerTestCase(TestCase):
    def setUp(self) -> None:
        self.user_1 = User.objects.create(id='test_id1', first_name='Test_first_name', last_name='Test_last_name',
                                          age=20,
                                          is_superuser=False, is_staff=False, password="test_password")
        self.data = UserSerializer(self.user_1).data
        self.expected_data = {
            'id': 'test_id1',
            'first_name': 'Test_first_name',
            'last_name': 'Test_last_name',
            'age': 20,
            'is_superuser': False,
            'is_staff': False,
            'username': '',
            'password': 'test_password'
        }
        self.invalid_data = {
            'id': 'test_id1',
            'first_name': 'Test_first_name',
            'last_name': '',
            'age': 20,
            'is_superuser': False,
            'is_staff': False,
            'username': '',
            'password': 'test_password'
        }

    def test_success(self):
        self.assertEqual(self.expected_data, self.data)

    def test_fail(self):
        serializer = UserSerializer(data=self.invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('last_name', serializer.errors)


class TicketsSerializerTestCase(TestCase):
    def setUp(self):
        self.user_1 = User.objects.create(id='test_user_id1', first_name='Test_first_name', last_name='Test_last_name',
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
        self.data = TicketsSerializer(self.ticket_1).data
        self.expected_data = {
            'id': 'test_id1',
            'event_id': 'test_event_id1',
            'user_id': 'test_user_id1',
            'is_inside': False
        }
        self.invalid_data = {
            'id': 'test_id1',
            'event_id': 'test_event_id1',
            'user_id': 'test_user_id1',
            'is_inside': "voshel"
        }

    def test_success(self):
        self.assertEqual(self.expected_data, self.data)

    def test_fail(self):
        serializer = TicketsSerializer(data=self.invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('is_inside', serializer.errors)


class RegisterSerializerTest(TestCase):
    def setUp(self):
        self.data = {
            'id': 'test_id1',
            'first_name': 'Test_first_name',
            'last_name': 'Test_last_name',
            'age': 20,
            'is_superuser': False,
            'is_staff': False,
            'email': 'test@test.ru',
            'password': 'test_password'
        }
        self.invalid_data = {
            'id': 'test_id1',
            'first_name': 'Test_first_name',
            'last_name': 'Test_last_name',
            'age': 20,
            'is_superuser': False,
            'is_staff': False,
            'password': 'test_password'
        }

    def test_valid_input(self):
        serializer = RegisterSerializer(data=self.data)
        self.assertTrue(serializer.is_valid())

    def test_invalid_input_data(self):
        serializer = RegisterSerializer(data=self.invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("email", serializer.errors)
