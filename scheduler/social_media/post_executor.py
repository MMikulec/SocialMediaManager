import asyncio
import pandas as pd
from scheduler.scheduling.async_task_scheduler import AsyncTaskScheduler
from scheduler.social_media.bot_manager import BotManager
from post_manager.bot_core.posts import SocialMediaPost
from logger_config import logger, console


class PostExecutor:
    def __init__(self, excel_file_name: str, dataframe: pd.DataFrame):
        """
        Initializes the PostExecutor with necessary attributes.

        :param excel_file_name: The name of the Excel file to use for bot management.
        """
        self.bot_manager = BotManager(excel_file_name)
        self.task_scheduler = AsyncTaskScheduler()
        self.df = dataframe

    async def start(self):
        """
        Start the event loop and continuously check the number of scheduled tasks.
        If there are no more tasks, stop the loop.
        """
        try:
            self.schedule_posts_from_dataframe()

            while True:
                await asyncio.sleep(1)
                if len(self.task_scheduler.get_jobs()) == 0:
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

        This method is used as a callback for the AsyncTaskScheduler to post content on the specified social media platform.

        :param platform: The platform on which to post.
        :param row:
        """
        logger.debug(f'Data to post:\nPosting to {platform}\nPost: \n{row}')

        # Load the bot for the specified platform
        bot = self.bot_manager.load_bot(platform)
        post = bot.create_post_from_dataframe_row(row)
        await bot.post(post)


"""
from scheduler.social_media.post_executor import PostExecutor
from datetime import datetime, timedelta
import asyncio
import pandas as pd 

async def main():
    # Create a DataFrame representing today's posts
    today_posts_df = pd.DataFrame({
        'Post ID': [1, 2, 3],
        'Platform': ['Instagram', 'Facebook', 'Instagram'],
        'Content': ['Check out our new product', 'New product launch', 'Product giveaway'],
        'Image Path': ['img1', 'img1', 'img1'],
        'Hashtags': ['#new #tech #insta', '#new #tech #fcbk', '#new #tech #insta'],
        'Scheduled Time': [datetime.now() + timedelta(minutes=1), datetime.now() + timedelta(minutes=0),
                           datetime.now() - timedelta(days=1)],
        'Status': ['Scheduled', 'Scheduled', 'Posted'],
        'Remarks': ['', '', '']
    })
    # Initialize the PostExecutor with the path to the Excel file
    post_executor = PostExecutor('path_to_your_excel_file.xlsx', dataframe=today_posts_df)
    # Schedule posts from the DataFrame
    await post_executor.schedule_posts_from_dataframe()

    # Keep the event loop running until all tasks are completed
    while asyncio.all_tasks():
        await asyncio.sleep(1)  # Sleep to avoid busy looping


async def run_main():
    await main()


if __name__ == '__main__':
    asyncio.run(run_main())
    
####################################x
from scheduler.social_media.post_executor import PostExecutor
from datetime import datetime, timedelta
import asyncio
import pandas as pd 
def main():
    # Create a DataFrame representing today's posts
    today_posts_df = pd.DataFrame({
        'Post ID': [1, 2, 3],
        'Platform': ['Instagram', 'Facebook', 'Instagram'],
        'Content': ['Check out our new product', 'New product launch', 'Product giveaway'],
        'Image Path': ['img1', 'img1', 'img1'],
        'Hashtags': ['#new #tech #insta', '#new #tech #fcbk', '#new #tech #insta'],
        'Scheduled Time': [datetime.now() + timedelta(minutes=1), datetime.now() + timedelta(minutes=0),
                           datetime.now() - timedelta(days=1)],
        'Status': ['Scheduled', 'Scheduled', 'Posted'],
        'Remarks': ['', '', '']
    })
    # Initialize the PostExecutor with the path to the Excel file
    post_executor = PostExecutor('path_to_your_excel_file.xlsx', dataframe=today_posts_df)
    # Schedule posts from the DataFrame
    asyncio.run(post_executor.start())
    
main()
    """
