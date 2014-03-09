import unittest

from pyramid import testing

from faapp.model import resources
from faapp.model import meta

class ViewTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    def test_my_view(self):
        from faapp.views import views
        request = testing.DummyRequest()
        info = views.top(resources.TopContext(request), request)
        self.assertEqual(info['models'], meta.model_names)

