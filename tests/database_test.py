import os
import unittest
from tinydb import TinyDB, Query

from app.database_helpers import *


class TestDatabaseHelpers(unittest.TestCase):
    db = TinyDB(os.path.join(os.path.dirname(__file__),
                'test_db.json')).table('schedules')

    def test_db_insert_schedule(self):
        db_insert_schedule(self.db, 'email1', 0, 0, ['MON'])
        self.assertEqual(len(self.db), 1)

        q = Query().fragment({'minute': 0, 'hour': 0, 'dow': ['MON']})
        self.assertTrue(self.db.contains(q))

        db_insert_schedule(self.db, 'email2', 0, 0, ['MON'])
        self.assertEqual(len(self.db), 1)

        result = self.db.search(q)
        self.assertTrue(len(result) > 0)
        self.assertEqual(result[0]['emails'], ['email1', 'email2'])

        self.db.truncate()
