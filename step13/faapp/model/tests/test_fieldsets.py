"""
    tests for ../__init__.py
"""

import unittest
from pyramid import testing

from faapp.model.fieldsets import (
        FieldSet,
    )

class PropertyHolder(object):
    pass

class DummyRequest(object):
    def __init__(self):
        pass


class Test_FieldSet(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    def test_init(self):
        request = DummyRequest()
        fs = FieldSet({"a": "a"}, request=request)

