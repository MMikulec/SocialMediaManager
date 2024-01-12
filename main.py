"""import pandas as pd
from rich import print
from rich.table import Table
from rich.console import Console

# Initialize Rich console
console = Console()

# Replace 'your_file.xlsx' with the path to your Excel file
excel_file = 'plan.xlsx'
df = pd.read_excel(excel_file)

# Display the first few rows of the dataframe using Rich
table = Table(show_header=True, header_style="bold magenta")
for column in df.columns:
    table.add_column(column)
for _, row in df.head().iterrows():
    table.add_row(*[str(item) for item in row])
console.print(table)

# Access a specific column
content_column = df['Content']

# Iterate through rows and print using Rich
for index, row in df.iterrows():
    console.print(f"[yellow]Výstup:[/yellow] {row['Post ID']} {row['Content']}")

# Filtering data
scheduled_posts = df[df['Status'] == 'Scheduled']
"""

from apscheduler.schedulers.background import BackgroundScheduler
from scheduler.scheduler import read_schedule_for_next_day
from rich.console import Console
import os

DEBUG = True
# Initialize Rich console
console = Console()

# Path to your Excel file
excel_file = 'plan.xlsx'

# Function to be called by the scheduler
def scheduled_reading():
    console.print(f"[cyan]Reading Excel file for scheduled posts...[/cyan]")
    scheduled_posts = read_schedule_for_next_day(excel_file)
    print(scheduled_posts)
    # Here you can add logic to handle these scheduled posts

# Initialize the scheduler
scheduler = BackgroundScheduler()

# Schedule to read Excel file every day at 23:00
scheduler.add_job(scheduled_reading, 'cron', hour=23, minute=0)

# Start the scheduler
scheduler.start()

# Debug mode: read Excel file immediately for testing
if DEBUG:
    scheduled_reading()

try:
    # This will keep the script running indefinitely while the scheduler runs in the background
    scheduler._event.wait()
except (KeyboardInterrupt, SystemExit):
    # Not strictly necessary if you're shutting down the whole script anyway
    scheduler.shutdown()

