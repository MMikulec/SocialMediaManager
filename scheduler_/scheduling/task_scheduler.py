from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from .event_listener import my_listener


class TaskScheduler:
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.scheduler.add_listener(my_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)

    def schedule_daily_loading(self, job_function):
        """Schedules daily loading of data."""
        self.scheduler.add_job(job_function, trigger=CronTrigger(hour=1, minute=0))

    def schedule_today_posts(self, job_function, posts):
        """Schedules posts for today."""
        for post in posts:
            self.scheduler.add_job(job_function, args=[post], trigger='date', run_date=post['Scheduled Time'])

    def start(self):
        """Starts the scheduler."""
        self.scheduler.start()

    def stop(self):
        """Stops the scheduler."""
        self.scheduler.shutdown()
