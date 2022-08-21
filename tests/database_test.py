import os
from tinydb import TinyDB, Query

from app.database_helpers import (
    db_insert_schedule,
    db_remove_schedule,
    db_insert_videos,
    db_insert_model,
    db_cleanup
)


class TestDatabaseHelpers():

    db_loc = os.path.join(os.path.dirname(__file__), 'test_db.json')

    def test_db_insert_schedule(self):
        db = TinyDB(self.db_loc).table('schedules')
        db.truncate()

        db_insert_schedule(db, 'email1', 0, 0, ['MON'])
        assert len(db) == 1

        q = Query().fragment({'minute': 0, 'hour': 0, 'dow': ['MON']})
        assert db.contains(q)

        db_insert_schedule(db, 'email2', 0, 0, ['MON'])
        assert len(db) == 1

        result = db.search(q)
        assert len(result) > 0
        assert result[0]['emails'] == ['email1', 'email2']
    # <-- End of test_db_insert_schedule()

    def test_db_remove_schedule(self):
        db = TinyDB(self.db_loc).table('schedules')
        db.truncate()

        db_insert_schedule(db, 'email1', 0, 0, ['MON'])
        assert len(db) == 1

        db_remove_schedule(db, 'email1')
        assert len(db) == 0

        db_insert_schedule(db, 'email1', 0, 0, ['MON'])
        db_insert_schedule(db, 'email2', 0, 0, ['MON'])
        db_insert_schedule(db, 'email3', 0, 0, ['MON'])
        assert len(db) == 1

        db_remove_schedule(db, 'email3')
        assert len(db) == 1

        q = Query().fragment({'minute': 0, 'hour': 0, 'dow': ['MON']})
        assert db.contains(q)

        result = db.search(q)
        assert len(result) > 0
        assert result[0]['emails'] == ['email1', 'email2']
    # <-- End of test_db_remove_schedule()

    def test_db_insert_video(self):
        db = TinyDB(self.db_loc).table('schedules')
        db.truncate()

        test1 = [
            {'id': 1, 'name': 'video1', 'link': 'link1', 'views': 0},
            {'id': 2, 'name': 'video2', 'link': 'link2', 'views': 0}
        ]
        assert db_insert_videos(db, test1)
        assert not db_insert_videos(db, test1)
        assert len(db) == 2

        test2 = [
            {'id': 1, 'name': 'video1', 'link': 'link1', 'views': 0},
            {'id': 2, 'name': 'video2', 'link': 'link2', 'views': 0},
            {'id': 3, 'name': 'video3', 'link': 'link3', 'views': 0},
            {'id': 4, 'name': 'video4', 'link': 'link4', 'views': 0}
        ]
        assert db_insert_videos(db, test2)
        assert not db_insert_videos(db, test2)
        assert len(db) == 4
    # <-- End of test_db_insert_video()

    def test_db_insert_model(self):
        db = TinyDB(self.db_loc).table('models')
        db.truncate()

        assert db_insert_model(db, 'model1', 'link1')
        assert db_insert_model(db, 'model2', 'link2', 'avatar2')
        assert not db_insert_model(db, 'model1', 'link1')
        assert len(db) == 2

        assert db.contains(Query()['model'] == 'model1')
        assert db.contains(Query()['model'] == 'model2')
        assert db.contains(Query()['avatar'] == 'avatar2')

        assert not db.contains(Query()['model'] == 'model3')
        assert not db.contains(Query()['avatar'] == 'avatar1')
    # <-- End of test_db_insert_model()

    def test_db_cleanup(self):
        db = TinyDB(self.db_loc).table('videos')
        test = [
            {'id': 1, 'name': 'video1', 'model': 'model1',
                'link': 'link1', 'views': 0},
            {'id': 2, 'name': 'video2', 'model': 'model2',
                'link': 'link2', 'views': 0},
            {'id': 3, 'name': 'video3', 'model': 'model3',
                'link': 'link3', 'views': 0},
            {'id': 4, 'name': 'video4', 'model': 'model4',
                'link': 'link4', 'views': 0}
        ]

        db.truncate()
        assert db_insert_videos(db, test)

        db_cleanup(db, {'model1': '', 'model2': '', 'model3': ''})
        assert db.contains(Query()['model'] == 'model1')
        assert not db.contains(Query()['model'] == 'model4')
        assert len(db) == 3

        db_cleanup(db, {})
        assert not db.contains(Query()['model'] == 'model2')
        assert not db.contains(Query()['model'] == 'model3')
        assert len(db) == 0
    # <-- End of test_db_cleanup()

# <-- End of TestDatabaseHelpers
