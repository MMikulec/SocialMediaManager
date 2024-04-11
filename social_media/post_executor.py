import asyncio
import pandas as pd
from pathlib import Path
from task_management.scheduling.async_task_scheduler import AsyncTaskScheduler
from data_management.data_holder import DataHolder
from social_media.bot_manager import BotManager
from logger_config import logger, console
from bot_manager.bot_core.errors import CredentialError


class PostExecutor:
    # TODO: 5. 4. 2024: file_path to source
    # TODO: 10. 4. 2024: dataframe to DataHolder
    def __init__(self, file_path: Path, data_holder: DataHolder):
        """
        Initializes the PostExecutor with necessary attributes.

        :param file_path: The path to the Excel file used for bot management.
        :param data_holder: The container holding the DataFrame of posts.
        """
        self.bot_manager = BotManager(file_path)
        self.task_scheduler = AsyncTaskScheduler()

        self.data_holder = data_holder
        self.current_df = self.data_holder.load_current_date_posts()

        # Track running tasks
        self.running_tasks = {}

    def update_executor(self, new_file_name: Path, new_data_holder: DataHolder):
        """
        Updates the PostExecutor with new attributes and re-initializes the AsyncTaskScheduler.

        :param new_file_name: The new name of the Excel file to use for bot management.
        :param  new_data_holder: The new DataHolder containing the updated DataFrame.
        """
        self.bot_manager = BotManager(new_file_name)

        self.data_holder = new_data_holder
        self.current_df = self.data_holder.load_current_date_posts()
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
            # Update data_holder with new data
            self.data_holder.update_data(self.current_df)
            # Stop the task scheduler
            self.task_scheduler.shutdown()

    def schedule_posts_from_dataframe(self):
        """
        Schedules posts from a pandas DataFrame.

        Iterates through the DataFrame rows and schedules each post based on its scheduled time, platform, and content.
        Only posts with a 'Scheduled' status are queued for posting.
        """
        # Iterate through the DataFrame rows
        for index, row in self.current_df.iterrows():

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
        # logger.debug(f"User name: {row['User Name']}")
        try:
            # logger.debug(f'Data to post:\nPosting to {platform}\nPost: \n{row}')

            # Load the bot for the specified platform and username
            bot = self.bot_manager.load_bot(row['User Name'], platform)
            post = bot.create_post_from_dataframe_row(row)
            # await bot.post(post)

            try:
                result = await bot.post(post)
            except CredentialError:
                pass
        finally:
            # Once execution is complete, mark it as not running
            self.running_tasks[row['Post ID']] = False
