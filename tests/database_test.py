import os
import unittest
from tinydb import TinyDB, Query

from app.database_helpers import *


class TestDatabaseHelpers(unittest.TestCase):
    path = os.path.join(os.path.dirname(__file__), 'test_db.json')

    def test_db_insert_schedule(self):
        db = TinyDB(self.path).table('schedules')
        if len(db) > 0:
            db.truncate()

        db_insert_schedule(db, 'email1', 0, 0, ['MON'])
        self.assertEqual(len(db), 1)

        q = Query().fragment({'minute': 0, 'hour': 0, 'dow': ['MON']})
        self.assertTrue(db.contains(q))

        db_insert_schedule(db, 'email2', 0, 0, ['MON'])
        self.assertEqual(len(db), 1)

        result = db.search(q)
        self.assertTrue(len(result) > 0)
        self.assertEqual(result[0]['emails'], ['email1', 'email2'])
    # <-- End of test_db_insert_schedule()

    def test_db_insert_video(self):
        db = TinyDB(self.path).table('videos')
        if len(db) > 0:
            db.truncate()

        test1 = [
            {'id': 1, 'name': 'video1', 'link': 'link1', 'views': 0},
            {'id': 2, 'name': 'video2', 'link': 'link2', 'views': 0}
        ]
        self.assertTrue(db_insert_videos(db, test1))
        self.assertFalse(db_insert_videos(db, test1))
        self.assertEqual(len(db), 2)

        test2 = [
            {'id': 1, 'name': 'video1', 'link': 'link1', 'views': 0},
            {'id': 2, 'name': 'video2', 'link': 'link2', 'views': 0},
            {'id': 3, 'name': 'video3', 'link': 'link3', 'views': 0},
            {'id': 4, 'name': 'video4', 'link': 'link4', 'views': 0}
        ]
        self.assertTrue(db_insert_videos(db, test2))
        self.assertFalse(db_insert_videos(db, test2))
        self.assertEqual(len(db), 4)
    # <-- End of test_db_insert_video()

    def test_db_insert_model(self):
        db = TinyDB(self.path).table('models')
        if len(db) > 0:
            db.truncate()

        self.assertTrue(db_insert_model(db, 'model1', 'link1'))
        self.assertTrue(db_insert_model(db, 'model2', 'link2', 'avatar2'))
        self.assertFalse(db_insert_model(db, 'model1', 'link1'))
        self.assertEqual(len(db), 2)

        self.assertTrue(db.contains(Query()['model'] == 'model1'))
        self.assertTrue(db.contains(Query()['model'] == 'model2'))
        self.assertTrue(db.contains(Query()['avatar'] == 'avatar1'))

        self.assertFalse(db.contains(Query()['model'] == 'model3'))
        self.assertFalse(db.contains(Query()['avatar'] == 'avatar2'))
    # <-- End of test_db_insert_model()

# <-- End of TestDatabaseHelpers
