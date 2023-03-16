from datetime import datetime

import pytz
from django.test import TestCase
from django_filters import CharFilter
from django_filters.rest_framework.filters import BooleanFilter

from api.models import Events, User, Tickets
from api.views import EventFilterSet


#

class EventFilterSetTest(TestCase):
    def setUp(self):
        d_start = datetime(2023, 10, 9, 23, 55, 59, 342380)
        d_end = datetime(2023, 10, 10, 13, 55, 59, 342380)
        self.events_1 = Events.objects.create(id='test1', title="Test Event", login="Test login",
                                              password="Test-password",
                                              address="Test address",
                                              time_start=d_start, time_end=d_end, max_guest_count=100,
                                              description="Test description")
        self.events_2 = Events.objects.create(id='someid', title="Some2 Event", login="Some2login",
                                              password="Some-password2",
                                              address="Some2 address",
                                              time_start=d_start, time_end=d_end, max_guest_count=200,
                                              description="Some2 description")

    def test_filter_ISNULL_lookup(self):
        f = Events._meta.get_field("title")
        result, params = EventFilterSet.filter_for_lookup(f, "icontain")
        self.assertEqual(result, CharFilter)
        self.assertDictEqual(params, {})
