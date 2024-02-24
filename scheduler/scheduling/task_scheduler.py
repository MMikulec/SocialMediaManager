from typing import Optional, Callable

import apscheduler.job
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from .event_listener import my_listener


class TaskScheduler:
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.scheduler.add_listener(my_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)
        self.jobs: dict[str, apscheduler.job.Job] = {}  # Mapping job names to Job objects

    def start(self):
        """Starts the scheduler."""
        self.scheduler.start()

    def stop(self):
        """Stops the scheduler."""
        self.scheduler.shutdown()

    def schedule_daily_loading(self, job_function: Callable, hour: int = 1, minute: int = 0, job_name: str | None = None) -> None:
        """
        Schedules daily loading of data with a customizable job ID.

        :param job_function: The function to schedule.
        :param hour: The hour at which the function should run.
        :param minute: The minute at which the function should run.
        :param job_name: The identifier for the scheduled job. Defaults to the name of the job_function.
        """
        # Use the function's name as the default ID if no ID is provided
        job_id = job_name if job_name is not None else job_function.__name__
        job = self.scheduler.add_job(job_function, trigger=CronTrigger(hour=hour, minute=minute), id=job_id)
        self.jobs[job_id] = job

    def schedule_today_posts(self, job_function, posts):
        """
        Schedules posts for today with unique job IDs based on post IDs.

        :param job_function: The function to execute for posting.
        :param posts: A list of post details to schedule.
        """
        for post in posts:
            job_id = f"post_{post['Post ID']}"  # Construct a unique job ID for each post
            job = self.scheduler.add_job(job_function, args=[post], trigger='date', run_date=post['Scheduled Time'],
                                         id=job_id)
            self.jobs[job_id] = job

    def remove_job(self, job_id):
        """
        Removes a job by its ID.

        :param job_id: The identifier of the job to remove.
        """
        if job_id in self.jobs:
            self.scheduler.remove_job(job_id)
            del self.jobs[job_id]
            print(f"Job {job_id} removed.")
        else:
            print(f"No job found with ID: {job_id}")

    def list_scheduled_jobs(self):
        """Lists all scheduled jobs and their next run times."""
        jobs = self.scheduler.get_jobs()
        print("Scheduled Jobs:")
        for job in jobs:
            print(f"ID: {job.id}, Next Run: {job.next_run_time}")

    def get_job(self, job_id):
        """
        Retrieves a job by its ID.

        :param job_id: The identifier of the job to retrieve.
        :return: The job instance if found, None otherwise.
        """
        return self.jobs.get(job_id, None)