import asyncio
import pandas as pd
from scheduler.scheduling.async_task_scheduler import AsyncTaskScheduler
from scheduler.social_media.bot_manager import BotManager
from post_manager.bot_core.posts import SocialMediaPost


class PostExecutor:
    def __init__(self, excel_file_name: str):
        """
        Initializes the PostExecutor with necessary attributes.

        :param excel_file_name: The name of the Excel file to use for bot management.
        """
        self.bot_manager = BotManager(excel_file_name)
        self.task_scheduler = AsyncTaskScheduler()

    async def schedule_posts_from_dataframe(self, dataframe: pd.DataFrame):
        """
        Schedules posts from a pandas DataFrame.

        Iterates through the DataFrame rows and schedules each post based on its scheduled time, platform, and content.
        Only posts with a 'Scheduled' status are queued for posting.

        :param dataframe: The pandas DataFrame containing post details. Expected columns are 'Post ID', 'Platform', 'Content',
                          'Image Path', 'Hashtags', 'Scheduled Time', 'Status', and 'Remarks'.
        """
        # Iterate through the DataFrame rows
        for index, row in dataframe.iterrows():
            # Assuming 'row' is a Series from your DataFrame
            social_media_post = SocialMediaPost.from_dataframe_row(row)

            # Schedule each post based on the DataFrame's information
            scheduled_time = row['Scheduled Time']  # Updated to correct column name
            platform = row['Platform']  # Updated to correct column name
            content = row['Content']  # Updated to correct column name

            # Only schedule if Status is 'Scheduled'
            if row['Status'] == 'Scheduled':
                # Schedule the post
                self.task_scheduler.add_job(
                    self.execute_post, 'date', run_date=scheduled_time, args=[platform, social_media_post]
                )

        self.task_scheduler.start()

    async def execute_post(self, platform: str, post: SocialMediaPost):
        """
        Executes a post using the appropriate bot based on the platform.

        This method is used as a callback for the AsyncTaskScheduler to post content on the specified social media platform.

        :param post: SocialMediaPost
        :param platform: The platform on which to post.
        """
        print(f'Posting to {platform} Post {post}')

        # Load the bot for the specified platform
        bot = self.bot_manager.load_bot(platform)

        """
        if bot:
            # Execute the post
            print(content)
            #await bot.post(content)  # Ensure this method is async or use run_in_executor for sync methods
        else:
            print(f"No bot found for platform {platform}")"""


"""
from scheduler.social_media.post_executor import PostExecutor
from datetime import datetime, timedelta
import asyncio
import pandas as pd 

async def main():
    # Initialize the PostExecutor with the path to the Excel file
    post_executor = PostExecutor('path_to_your_excel_file.xlsx')
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
    # Schedule posts from the DataFrame
    await post_executor.schedule_posts_from_dataframe(today_posts_df)

    # Keep the event loop running until all tasks are completed
    while asyncio.all_tasks():
        await asyncio.sleep(1)  # Sleep to avoid busy looping


async def run_main():
    await main()


if __name__ == '__main__':
    asyncio.run(run_main())
    """
