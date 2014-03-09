import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import (
    sessionmaker,
)

from pyramid import testing
from ..model.meta import (
    Address, Person,
    )

class ModelTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    def test_my_model(self):
        return
        engine = create_engine("sqlite://")

        db = sessionmaker(
            bind=engine,
        )()

        # now I have my db (session) and can do whatever I want with it
        res = db.query(Address).filter(Address.line1=="one").all()

        self.assertEqual(len(res), 0)

