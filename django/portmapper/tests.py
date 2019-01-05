from django.test import TestCase
from django.urls import reverse


class TestGets(TestCase):
    def setUp(self):
        self.views = ['services_list', 'clusters_list']

    def test_views(self):
        for view in self.views:
            print('Testing reverse for view: %s' % view)
            response = self.client.get(reverse(view))
            self.assertEqual(response.status_code, 200)
