from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from functools import wraps
import asyncio


class AsyncTaskScheduler(AsyncIOScheduler):
    def __init__(self):
        super().__init__()
        self.add_listener(self._my_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)
        self.jobs = {}

    def _my_listener(self, event):
        # Your custom listener logic for asynchronous context
        pass

    def job(self, trigger, **trigger_args):
        def decorator(func):
            @wraps(func)
            async def wrapper(*args, **kwargs):
                await func(*args, **kwargs)  # Ensure the wrapped function supports async call

            job_id = trigger_args.pop('id', func.__name__)
            job = self.add_job(wrapper, trigger, id=job_id, **trigger_args)
            self.jobs[job_id] = job
            return wrapper

        return decorator
