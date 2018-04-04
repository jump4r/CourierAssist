from django.test import TestCase
from api.views import JsonActivity
from datetime import datetime

# Create your tests here.
class JsonActivityTestCase(TestCase):
    def setUp(self):
        pass
        #test

    def test_time_equality(self):
        a = JsonActivity(1, '', 1, datetime(1970, 1, 1))
        test_time = datetime(1970, 1, 1)
        self.assertEqual(JsonActivity.timeDifference(a, test_time), 0)
