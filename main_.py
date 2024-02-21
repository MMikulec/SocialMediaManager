from scheduler_ import ExcelDataManager, LogDataManager, TaskScheduler, PostExecutor, BotManager, display_dataframe_as_table

excel_file_path = r"plan.xlsx"
excel_data_manager = ExcelDataManager(excel_file_path)

logs_directory = r"\post_manager\bots"
log_data_manager = LogDataManager(logs_directory)