# scheduler/scheduler.py

import pandas as pd
from datetime import datetime, timedelta


def read_schedule_for_next_day(excel_file):
    # Read the Excel file
    df = pd.read_excel(excel_file)

    # Get current date and next date
    current_date = datetime.now().date()
    next_date = current_date + timedelta(days=1)

    # Filter posts scheduled for the next day
    next_day_posts = df[(df['Scheduled Time'].dt.date == next_date) & (df['Status'] == 'Scheduled')]
    print("nEXT", next_day_posts)
    return next_day_posts
