import pytest
from pathlib import Path
import pandas as pd
from datetime import datetime, timedelta
from scheduler.data_manager.log_data_manager import LogDataManager  # Adjust the import path according to your project structure


@pytest.fixture
def sample_log_file(tmp_path):
    """Fixture to create a temporary log file with sample log entries for testing."""
    content = """\
2024-02-16 11:54:00,303 - DEBUG - plan.xlsx - Facebook - Post ID: 1 - Posted - message from app
2024-02-16 11:54:00,318 - DEBUG - plan.xlsx - Instagram - Post ID: 2 - Posted - message from app
2024-02-16 11:54:00,438 - DEBUG - plan.xlsx - Instagram - Post ID: 3 - Error - message from app
2024-02-16 11:54:00,478 - DEBUG - plan.xlsx - Facebook - Post ID: 4 - Error - message from app
"""
    log_file = tmp_path / "sample.log"
    log_file.write_text(content)
    return log_file


@pytest.fixture
def sample_df():
    """Fixture to create a sample DataFrame similar to the one used by ExcelDataManager."""
    df = pd.DataFrame({
        'Post ID': [1, 2, 3, 4],
        'Status': ['Scheduled', 'Scheduled', 'Scheduled', 'Scheduled'],
    })
    return df


def test_update_df_from_logs(sample_log_file, sample_df):
    """Test updating a DataFrame based on log entries."""
    log_manager = LogDataManager(log_file_path=sample_log_file)
    updated_df = log_manager.update_df_from_logs(sample_df, only_today=False)

    # Define expected outcomes based on the log file content
    expected_statuses = ['Posted', 'Posted', 'Error', 'Error']
    assert all(updated_df['Status'] == expected_statuses), "The statuses should be updated according to the log file."
