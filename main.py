import time
from pathlib import Path
from logger_config import logger, console

from scheduler import ExcelDataManager, LogDataManager, TaskScheduler, PostExecutor, BotManager, \
    display_dataframe_as_table


def main():
    excel_file_path = Path("plan.xlsx")
    log_file_path = Path(f'post_manager/logs/{excel_file_path.stem}_posts.log')

    excel_manager = ExcelDataManager(excel_file_path)
    log_manager = LogDataManager(log_file_path)

    # Update Excel with all available logs at start-up
    excel_manager.df = log_manager.update_df_from_logs(excel_manager.df, only_today=False)

    def update_excel_from_logs():
        """Updates the Excel file with today's logs and saves changes."""
        excel_manager.df = log_manager.update_df_from_logs(excel_manager.df, only_today=True)
        excel_manager.save_changes_to_excel()

    def load_excel():
        """Loads today's posts from Excel and displays them."""
        excel_manager.load_excel_data()
        display_dataframe_as_table(excel_manager.load_current_date_posts(), "Today's posts")

    # Initialize the scheduler and configure tasks
    excel_task_scheduler = TaskScheduler()
    excel_task_scheduler.schedule_daily_loading(update_excel_from_logs, hour=23, minute=0)
    # Assuming you want to load and display today's posts at a specific time, default at 01:00
    excel_task_scheduler.schedule_daily_loading(load_excel)
    excel_task_scheduler.start()
    excel_task_scheduler.list_scheduled_jobs()


    #posts_task_scheduler = TaskScheduler()


if __name__ == "__main__":
    main()

    # Keep the script running to keep the scheduler active
    try:
        while True:
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        pass
