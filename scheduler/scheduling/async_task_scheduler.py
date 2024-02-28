from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from functools import wraps
import asyncio

from apscheduler.triggers.date import DateTrigger


class AsyncTaskScheduler:
    def __init__(self):
        # Make the scheduler private and asynchronous
        self._scheduler = AsyncIOScheduler()
        self._scheduler.add_listener(self._my_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)
        self.jobs = {}

    def _my_listener(self, event):
        # Custom listener logic
        # Ensure this method can handle async operations if needed
        pass

    def job(self, trigger, **trigger_args):
        def decorator(func):
            @wraps(func)
            async def wrapper(*args, **kwargs):
                # Ensure the wrapped function supports async call
                await func(*args, **kwargs)

            # Determine the job ID: use the 'id' from trigger_args if present, otherwise use the function name
            job_id = trigger_args.pop('id', func.__name__)

            # Now, since we've explicitly removed 'id' from trigger_args, we can safely pass it without conflict
            # Note: APScheduler does not support async jobs natively; if func is an async function,
            # you may need to wrap the execution in a separate async function that handles event loop execution.
            job = self._scheduler.add_job(wrapper, trigger, id=job_id, **trigger_args)
            self.jobs[job_id] = job
            return wrapper

        return decorator

    def start(self):
        """Starts the scheduler."""
        # No changes needed here for starting the scheduler in an async environment
        self._scheduler.start()

    def stop(self):
        """Stops the scheduler."""
        # No changes needed here for stopping the scheduler in an async environment
        self._scheduler.shutdown()

    async def list_scheduled_jobs(self):
        """Lists all scheduled jobs."""
        # Make this function asynchronous if you plan to perform async operations within
        jobs = self._scheduler.get_jobs()
        print("Scheduled Jobs:")
        for job in jobs:
            print(f"ID: {job.id}, Next Run: {job.next_run_time}")

    async def remove_job(self, job_id):
        """Removes a job by its ID."""
        # Make this function asynchronous if you plan to perform async operations within
        if job_id in self.jobs:
            self._scheduler.remove_job(job_id)
            del self.jobs[job_id]
            print(f"Job {job_id} removed.")
        else:
            print(f"No job found with ID: {job_id}")

    async def add_job(self, func, trigger_type, **kwargs):
        """Adds a new job to the async task scheduler.

        Args:
            func (callable): The asynchronous function to be scheduled.
            trigger_type (str): The type of trigger ('date', 'interval', 'cron', etc.).
            **kwargs: Additional keyword arguments for the scheduler and the job.
        """
        # Determine the trigger based on the type and provided arguments
        if trigger_type == 'date':
            # For date triggers, 'run_date' must be provided in kwargs
            if 'run_date' not in kwargs:
                raise ValueError("run_date is required for date triggers")
            trigger = DateTrigger(run_date=kwargs['run_date'])
        elif trigger_type == 'interval':
            # For interval triggers, 'seconds', 'minutes', or other time intervals should be provided
            trigger = kwargs  # Interval triggers can directly use kwargs
        elif trigger_type == 'cron':
            # For cron triggers, check for necessary cron fields in kwargs
            trigger = CronTrigger(**kwargs)
        else:
            raise ValueError(f"Unsupported trigger type: {trigger_type}")

        # Schedule the job with the determined trigger
        job = self._scheduler.add_job(func, trigger, **kwargs)
        job_id = kwargs.get('id', job.id)  # Use provided ID or default to job's ID
        self.jobs[job_id] = job
        return job_id  # Return the job ID for reference

# TODO: 28. 2. 2024: try rewrite AsyncTaskScheduler and TaskScheduler
class AsyncTaskSchedulerTest(AsyncIOScheduler):
    def __init__(self):
        super().__init__()