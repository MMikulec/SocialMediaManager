import asyncio
import pandas as pd
from pathlib import Path
from task_management.scheduling.async_task_scheduler import AsyncTaskScheduler
from social_media.bot_manager import BotManager
from logger_config import logger, console
from bot_manager.bot_core.errors import CredentialError


class PostExecutor:
    def __init__(self, file_path: Path, dataframe: pd.DataFrame):
        """
        Initializes the PostExecutor with necessary attributes.

        :param file_path: The name of the Excel file to use for bot management.
        """
        self.bot_manager = BotManager(file_path.name)
        self.task_scheduler = AsyncTaskScheduler()
        self.df = dataframe
        # Track running tasks
        self.running_tasks = {}

        # Derive the credentials file path from the Excel file name
        # This assumes both files are in the same directory and credentials file has a .json extension
        self.credentials_file_path = file_path.with_suffix('.json')

        # Initialize an empty auth manager; we'll set this up properly in an async method
        self.auth_manager = None

    def update_executor(self, new_excel_file_name: str, new_dataframe: pd.DataFrame):
        """
        Updates the PostExecutor with new attributes and re-initializes the AsyncTaskScheduler.

        :param new_excel_file_name: The new name of the Excel file to use for bot management.
        :param new_dataframe: The new DataFrame containing the posts data.
        """
        self.bot_manager = BotManager(new_excel_file_name)
        self.df = new_dataframe
        self.task_scheduler = AsyncTaskScheduler()
        self.running_tasks = {}

    async def start(self):
        """
        Start the event loop and continuously check the number of scheduled tasks.
        If there are no more tasks, stop the loop.
        """
        try:
            self.schedule_posts_from_dataframe()

            while True:
                await asyncio.sleep(5)
                # Check if there are no more scheduled jobs and all running tasks are completed
                if not self.task_scheduler.get_jobs() and all(not status for status in self.running_tasks.values()):
                    break
        except KeyboardInterrupt:
            # Handle keyboard interrupt if needed
            pass
        finally:
            # Stop the task scheduler
            self.task_scheduler.shutdown()

    def schedule_posts_from_dataframe(self):
        """
        Schedules posts from a pandas DataFrame.

        Iterates through the DataFrame rows and schedules each post based on its scheduled time, platform, and content.
        Only posts with a 'Scheduled' status are queued for posting.
        """
        # Iterate through the DataFrame rows
        for index, row in self.df.iterrows():

            # Schedule each post based on the DataFrame's information
            scheduled_time = row['Scheduled Time']  # Updated to correct column name
            platform = row['Platform']  # Updated to correct column name

            # Only schedule if Status is 'Scheduled'
            if row['Status'] == 'Scheduled':
                # Schedule the post
                self.task_scheduler.add_job(
                    self.execute_post, 'date', run_date=scheduled_time, args=[platform, row]
                )

        self.task_scheduler.start()

    async def execute_post(self, platform: str, row: pd.Series):
        """
        Executes a post using the appropriate bot based on the platform.

        This method is used as a callback for the AsyncTaskScheduler
        to post content on the specified social media platform.

        :param platform: The platform on which to post.
        :param row:
        """
        # Before starting the actual execution, mark this task as running
        self.running_tasks[row['Post ID']] = True
        try:
            logger.debug(f'Data to post:\nPosting to {platform}\nPost: \n{row}')

            # Load the bot for the specified platform
            bot = self.bot_manager.load_bot(platform)
            post = bot.create_post_from_dataframe_row(row)
            # await bot.post(post)

            # # TODO: Create except with code, which update credentials data.
            try:
                result = await bot.post(post)
            except CredentialError:
                pass
        finally:
            # Once execution is complete, mark it as not running
            self.running_tasks[row['Post ID']] = False
