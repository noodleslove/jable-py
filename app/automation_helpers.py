from crontab import CronTab


class Scheduler:

    def __init__(self, file_name):
        self.cron = CronTab(tab=file_name)
        self.file_name = file_name
    # <-- End of __init__()

    def add_job(
        self,
        command: str,
        comment: str,
        minute: int = 0,
        hour: int = 0,
        dow: list[str] = None
    ) -> None:
        """Add a new job with the given frequency to the Cron

        Args:
            command (str): The command to execute
            comment (str): Specify the email address for removal later
            minute (int, optional): At which minute the job will be executed.
                Defaults to 0.
            hour (int, optional): At which hour the job will be executed.
                Defaults to 0.
            dow (list[str], optional): At which day of week the job will be 
                executed. `['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN']`
                Defaults to None.
        """
        job = self.cron.new(command=command, comment=comment)
        job.minute.on(minute)
        job.hour.on(hour)

        if dow is not None:
            job.dow.on(*dow)
        else:
            job.every().dows()

        # self.cron.write(user=True)
        self.cron.write(self.file_name)
    # <-- End of add_job()

    def remove_job(self, comment: str):
        """Remove all jobs for given email address

        Args:
            comment (str): The email address to remove
        """
        self.cron.remove_all(comment=comment)
        # self.cron.write(user=True)
        self.cron.write(self.file_name)
    # <-- End of remove_job()

    def list_all_job(self):
        """Return a list of all active jobs

        Returns:
            list: A list of all active jobs
        """
        return [job for job in self.cron]
    # <-- End of list_all_job()

# <-- End of Scheduler
