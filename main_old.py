import time
from scheduler_old.scheduler import ExcelScheduler
from logger_config import logger, console
import logging


if logging.DEBUG:
    logger.warning(f"Is running in DEBUG mode")


# Path to your Excel file
excel_file = 'plan.xlsx'
scheduler1 = ExcelScheduler(excel_file)
scheduler1.start()

# Keep the script running to keep the scheduler active
try:
    while True:
        time.sleep(1)
except (KeyboardInterrupt, SystemExit):
    scheduler1.stop()
