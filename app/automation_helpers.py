from crontab import CronTab


class Scheduler:

    def __init__(self):
        self.cron = CronTab(user=True)
    # <-- End of __init__()

    def add_job(
        self,
        command: str,
        comment: str,
        minute: int = 0,
        hour: int = 0,
        dow: list[str] = None
    ) -> None:
        job = self.cron.new(command=command, comment=comment)
        job.minute.on(minute)
        job.hour.on(hour)

        if dow is not None:
            job.dow.on(*dow)
        else:
            job.every().dows()

        self.cron.write()
    # <-- End of add_job()

    def remove_job(self, comment: str):
        self.cron.remove_all(comment=comment)
        self.cron.write()
    # <-- End of remove_job()

    def list_all_job(self):
        return [job for job in self.cron]
    # <-- End of list_all_job()

# <-- End of Scheduler
