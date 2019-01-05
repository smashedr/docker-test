from django.test import TestCase
from django.urls import reverse


class TestBasic(TestCase):
    def setUp(self):
        self.views = {
            'home:index': 200,
            'home:about': 200,
            'login:show': 200,
            'login:login': 405,
            'login:logout': 405,
            'home:profile': 302,
            'admin:index': 302,
        }

    def test_views(self):
        for view, status in self.views.items():
            print('Testing view "{}" for code "{}"'.format(view, status))
            response = self.client.get(reverse(view))
            self.assertEqual(response.status_code, status)
