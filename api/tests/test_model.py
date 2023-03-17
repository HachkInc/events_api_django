from datetime import datetime
from sqlite3 import IntegrityError

import pytz
from django.test import TestCase

from api.models import Events, User, Tickets


class EventsModelTestCase(TestCase):

    def setUp(self) -> None:
        self.d_start = datetime(2023, 10, 9, 23, 55, 59, 342380, tzinfo=pytz.UTC)
        self.d_end = datetime(2023, 10, 10, 13, 55, 59, 342380, tzinfo=pytz.UTC)
        self.event_1 = Events.objects.create(id='test_id1', title='Test Event', login='Test login',
                                             password='Test-password',
                                             address='Test address',
                                             time_start=self.d_start, time_end=self.d_end, max_guest_count=100,
                                             description='Test description')

    def test_success_create_event(self):
        self.assertEqual("Test Event", self.event_1.title)
        self.assertEqual("Test login", self.event_1.login)
        self.assertEqual("Test-password", self.event_1.password)
        self.assertEqual("Test address", self.event_1.address)
        self.assertEqual(self.d_start, self.event_1.time_start)
        self.assertEqual(self.d_end, self.event_1.time_end)
        self.assertEqual("Test description", self.event_1.description)

    def test_fail_create_event(self):
        with self.assertRaises(Exception):
            event1 = Events.objects.create()


class UserModelTestCase(TestCase):

    def setUp(self) -> None:
        self.user_1 = User.objects.create(id='test_id11', first_name='Test_first_name', last_name='Test_last_name',
                                          age=20,
                                          is_superuser=False, is_staff=False, password="test_password")

    def test_success_create_user(self):
        self.assertEqual('test_id11', self.user_1.id)
        self.assertEqual("Test_first_name", self.user_1.first_name)
        self.assertEqual("Test_last_name", self.user_1.last_name)
        self.assertEqual("test_password", self.user_1.password)
        self.assertEqual(False, self.user_1.is_staff)
        self.assertEqual(False, self.user_1.is_superuser)
        self.assertEqual(20, self.user_1.age)

    def test_fail_create_user(self):
        with self.assertRaises(Exception):
            user1 = User.objects.create()


class TicketModelTestCase(TestCase):

    def setUp(self) -> None:
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

    def test_success_create_ticket(self):
        self.assertEqual('test_id1', self.ticket_1.id)
        self.assertEqual('test_event_id1', self.ticket_1.event_id.id)
        self.assertEqual('test_user_id1', self.ticket_1.user_id.id)

    def test_fail_create_event(self):
        with self.assertRaises(Exception):
            ticket1 = Tickets.objects.create()
