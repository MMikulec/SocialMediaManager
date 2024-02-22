import time
from pathlib import Path
from logger_config import logger, console

from scheduler_ import ExcelDataManager, LogDataManager, TaskScheduler, PostExecutor, BotManager, \
    display_dataframe_as_table


def main():
    excel_file_path = Path("plan.xlsx")
    excel_manager = ExcelDataManager(excel_file_path)
    display_dataframe_as_table(excel_manager.load_current_date_posts(), "Today's posts")

    log_file_path = Path(f'post_manager/logs/{excel_file_path.name}_posts.log')
    log_manager = LogDataManager(log_file_path)
    updated_df = log_manager.update_df_from_logs(excel_manager.df, only_today=True)
    excel_manager.df = updated_df

    # ######################################
    excel_task_scheduler = TaskScheduler()
    excel_task_scheduler.schedule_daily_loading(excel_manager.load_excel_data)
    excel_task_scheduler.start()

    posts_task_scheduler = TaskScheduler()


if __name__ == "__main__":
    main()

    # Keep the script running to keep the scheduler active
    try:
        while True:
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        pass
