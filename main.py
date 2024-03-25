import asyncio
import time
from pathlib import Path
from logger_config import logger, console

from task_management import ExcelDataManager, LogDataManager, TaskScheduler, display_dataframe_as_table
from social_media import PostExecutor


def main():
    excel_file_path = Path("plan.xlsx")
    log_file_path = Path(f'bot_manager/logs/{excel_file_path.stem}_posts.log')

    excel_manager = ExcelDataManager(excel_file_path)
    log_manager = LogDataManager(log_file_path)

    # Update Excel with all available logs at start-up
    excel_manager.df = log_manager.update_df_from_logs(excel_manager.df, only_today=False)
    display_dataframe_as_table(excel_manager.load_current_date_posts(), "Today's posts")

    # Initialize the scheduler and configure tasks using the TaskScheduler class
    excel_task_scheduler = TaskScheduler()

    # Initialize post executor and load current data
    post_task_executor = PostExecutor(excel_file_path, excel_manager.load_current_date_posts())
    asyncio.run(post_task_executor.start())

    @excel_task_scheduler.job('cron', hour=23, minute=0, id='update_excel')
    def update_excel_from_logs():
        """Updates the Excel file with today's logs and saves changes."""
        excel_manager.df = log_manager.update_df_from_logs(excel_manager.df, only_today=True)
        excel_manager.save_changes_to_excel()

    @excel_task_scheduler.job('cron', hour=1, minute=0, id='load_excel')
    def load_excel():
        """Loads today's posts from Excel and displays them."""
        excel_manager.load_excel_data()
        display_dataframe_as_table(excel_manager.load_current_date_posts(), "Today's posts")

        post_task_executor.update_executor(excel_file_path.name, excel_manager.load_current_date_posts())
        asyncio.run(post_task_executor.start())

    excel_task_scheduler.start()
    print(excel_task_scheduler.get_jobs())


if __name__ == "__main__":
    main()

    # Keep the script running to keep the scheduler active
    try:
        while True:
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        pass
