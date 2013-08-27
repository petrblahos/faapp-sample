import unittest

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
        from sqlalchemy import create_engine
        engine = create_engine("sqlite://")
        db = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
        db.configure(bind=engine)
        # now I have my db (session) and can do whatever I want with it
        res = db.query(MyModel).filter(MyModel.name=="one").all()

        self.assertEqual(len(res), 1)
        self.assertEqual(res[0].id, 1)

