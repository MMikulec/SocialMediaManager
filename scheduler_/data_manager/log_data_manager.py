import os
from datetime import datetime


class LogDataManager:
    def __init__(self, logs_directory: str):
        self.logs_directory = logs_directory

    def read_log_entries(self, only_today: bool = False):
        """Reads log entries, optionally filtering for today's entries."""
        log_entries = []
        for log_file in os.listdir(self.logs_directory):
            if log_file.endswith('.log'):
                with open(os.path.join(self.logs_directory, log_file), 'r') as file:
                    for line in file:
                        if only_today and not self.is_entry_for_today(line):
                            continue
                        entry = self.parse_log_line(line)
                        if entry:
                            log_entries.append(entry)
        return log_entries

    def is_entry_for_today(self, line):
        """Checks if a log entry line corresponds to the current date."""
        log_date_str = line.split()[0]
        try:
            log_date = datetime.strptime(log_date_str, '%Y-%m-%d').date()
            return log_date == datetime.now().date()
        except ValueError:
            return False

    def parse_log_line(self, line):
        """Parses a log line into a structured format."""
        # Implement parsing logic based on your log format
        return {'post_id': '...', 'status': '...'}
