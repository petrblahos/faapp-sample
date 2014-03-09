"""
    tests for ../__init__.py
"""

import unittest
from pyramid import testing

class PropertyHolder(object):
    pass

class DummyRequest(object):
    def __init__(self):
        self.sessionmaker_called = 0
        self.add_finished_callback_called = 0
        self.registry = PropertyHolder()
        self.registry.sessionmaker = self.sessionmaker
    def sessionmaker(self):
        self.sessionmaker_called+= 1
        return "SESSION-FACTORY"
    def add_finished_callback(self, cb):
        self.add_finished_callback_called+= 1


class Test_db(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    def test_db(self):
        from .. import db
        request = DummyRequest()
        self.assertEqual("SESSION-FACTORY", db(request))
        self.assertEqual(request.sessionmaker_called, 1)
        self.assertEqual(request.add_finished_callback_called, 1)

