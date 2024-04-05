import re
from datetime import datetime
from pathlib import Path


class LogDataManager:
    def __init__(self, log_file_path: Path):
        """
        Initializes the LogDataManager with the path to the log file.

        :param log_file_path: Path to the log file.
        """
        self.log_file_path = log_file_path
        self.ensure_log_file_exists()

    def ensure_log_file_exists(self):
        """
        Ensures the log file exists by creating an empty file if it does not exist.
        """
        if not self.log_file_path.exists():
            self.log_file_path.touch()

    def read_logs(self, only_today=False):
        """
        Reads the log entries, optionally filtering for entries from today.

        :param only_today: Whether to return only today's log entries.
        :return: A list of dictionaries, each containing data from a log entry.
        """
        log_entries = []
        today = datetime.now().date()
        with open(self.log_file_path, 'r') as log_file:
            for line in log_file:
                if only_today:
                    log_date = datetime.strptime(line.split()[0], '%Y-%m-%d').date()
                    if log_date != today:
                        continue
                match = re.search(r'Post ID: (\d+) - (\w+)(?=\s-)', line)
                if match:
                    post_id, status = match.groups()
                    log_entries.append({'post_id': int(post_id), 'status': status})
        return log_entries

    def update_df_from_logs(self, df, only_today=False):
        """
        Updates a DataFrame based on the log entries.

        :param df: The DataFrame to update.
        :param only_today: Whether to update the DataFrame based on only today's log entries.
        :return: The updated DataFrame.
        """
        if df is None or df.empty:
            return df  # Return the original DataFrame if it's None or empty

        log_entries = self.read_logs(only_today=only_today)
        for entry in log_entries:
            # Assuming the DataFrame has columns 'Post ID' and 'Status'
            # And the log entries dictionary has keys 'post_id' and 'status'
            if entry['post_id'] in df['Post ID'].values:
                df.loc[df['Post ID'] == entry['post_id'], 'Status'] = entry['status']

        return df
