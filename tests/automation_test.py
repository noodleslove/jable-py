import os
import unittest

from app.scraper import Scraper
from app.automation_helpers import *


class TestAutomation(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestAutomation, self).__init__(*args, **kwargs)
        self.path = os.path.join(os.path.dirname(__file__), 'test_jobs.tab')

    def test_add_job(self):
        os.remove(self.path)
        schedule = Scheduler(self.path)

        schedule.add_job('command1', 'comment1', 0, 0, ['MON'])
        self.assertEqual(len(schedule.cron), 1)

        schedule.add_job('command2', 'comment2', 0, 0, ['MON'])
        schedule.add_job('command3', 'comment3', 0, 0, ['MON'])
        schedule.add_job('command4', 'comment4', 0, 0, ['MON'])
        self.assertEqual(len(schedule.cron), 4)

    def test_remove_job(self):
        os.remove(self.path)
        schedule = Scheduler(self.path)

        schedule.add_job('command1', 'comment1', 0, 0, ['MON'])
        self.assertEqual(len(schedule.cron), 1)
        schedule.remove_job('comment1')
        self.assertEqual(len(schedule.cron), 0)

        schedule.add_job('command2', 'comment2', 0, 0, ['MON'])
        schedule.add_job('command3', 'comment3', 0, 0, ['MON'])
        schedule.add_job('command4', 'comment4', 0, 0, ['MON'])
        schedule.remove_job('comment4')
        self.assertEqual(len(schedule.cron), 2)
