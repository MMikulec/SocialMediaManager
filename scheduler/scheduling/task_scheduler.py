from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from functools import wraps


class TaskScheduler:
    def __init__(self):
        # Make the scheduler private
        self._scheduler = BackgroundScheduler()
        self._scheduler.add_listener(self._my_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)
        self.jobs = {}

    def _my_listener(self, event):
        # Custom listener logic
        pass

    def job(self, trigger, **trigger_args):
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)

            # Determine the job ID: use the 'id' from trigger_args if present, otherwise use the function name
            job_id = trigger_args.pop('id', func.__name__)

            # Now, since we've explicitly removed 'id' from trigger_args, we can safely pass it without conflict
            job = self._scheduler.add_job(wrapper, trigger, id=job_id, **trigger_args)
            self.jobs[job_id] = job
            return wrapper

        return decorator

    def start(self):
        """Starts the scheduler."""
        self._scheduler.start()

    def stop(self):
        """Stops the scheduler."""
        self._scheduler.shutdown()

    def list_scheduled_jobs(self):
        """Lists all scheduled jobs."""
        jobs = self._scheduler.get_jobs()
        print("Scheduled Jobs:")
        for job in jobs:
            print(f"ID: {job.id}, Next Run: {job.next_run_time}")

    def remove_job(self, job_id):
        """Removes a job by its ID."""
        if job_id in self.jobs:
            self._scheduler.remove_job(job_id)
            del self.jobs[job_id]
            print(f"Job {job_id} removed.")
        else:
            print(f"No job found with ID: {job_id}")
