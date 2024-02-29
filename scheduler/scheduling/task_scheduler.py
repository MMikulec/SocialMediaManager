from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from functools import wraps


class TaskScheduler(BackgroundScheduler):
    def __init__(self):
        super().__init__()
        self.add_listener(self._my_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)
        self.jobs = {}

    def _my_listener(self, event):
        # Custom listener logic remains the same
        pass

    def job(self, trigger, **trigger_args):
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)

            # Use the base class's 'add_job' directly
            job_id = trigger_args.pop('id', func.__name__)
            job = self.add_job(wrapper, trigger, id=job_id, **trigger_args)
            self.jobs[job_id] = job
            return wrapper

        return decorator
