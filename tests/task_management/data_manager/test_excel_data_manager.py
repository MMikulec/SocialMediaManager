# test_excel_data_manager.py
import pandas as pd
from datetime import datetime, timedelta
from pandas.testing import assert_frame_equal

import pytest
# Adjust the import according to your project structure
from task_management.data_manager.excel_data_manager import ExcelDataManager


# Create a fixture for the ExcelDataManager
@pytest.fixture
def temp_excel_file(tmp_path):
    """Fixture to create a temporary Excel file with detailed data for testing."""
    df = pd.DataFrame({
        'Post ID': [1, 2, 3],
        'Platform': ['Instagram', 'Facebook', 'Instagram'],
        'Content': ['Check out our new product', 'New product launch', 'Product giveaway'],
        'Image Path': ['img1', 'img1', 'img1'],
        'Hashtags': ['#new #tech #insta', '#new #tech #fcbk', '#new #tech #insta'],
        'Scheduled Time': [datetime.now() + timedelta(days=1), datetime.now(), datetime.now() - timedelta(days=1)],
        'Status': ['Scheduled', 'Scheduled', 'Posted'],
        'Remarks': ['', '', '']
    })
    # Convert 'Scheduled Time' to the appropriate datetime format
    df['Scheduled Time'] = pd.to_datetime(df['Scheduled Time'])
    file_path = tmp_path / "test_schedule.xlsx"
    df.to_excel(file_path, index=False)
    return file_path


@pytest.fixture
def excel_manager(temp_excel_file):
    """Fixture to initialize ExcelDataManager with the temporary Excel file."""
    return ExcelDataManager(excel_file_path=temp_excel_file, sheet_name='Sheet1',
                            id_column='Post ID', status_column='Status',
                            date_column='Scheduled Time')


def test_load_excel_data(excel_manager):
    """Test loading data from Excel."""
    excel_manager.load_excel_data()
    assert isinstance(excel_manager.df, pd.DataFrame)
    assert not excel_manager.df.empty


def test_load_current_date_posts(excel_manager):
    """Test loading posts for the current date."""
    today_posts = excel_manager.load_current_date_posts()
    assert today_posts is not None
    assert all(today_posts['Scheduled Time'].dt.date == datetime.now().date())


def test_update_main_dataframe(excel_manager):
    """Test updating the main DataFrame with a subset DataFrame."""
    # Create an updated DataFrame for Post ID 2
    updated_df = pd.DataFrame({
        'Post ID': [2],
        'Status': ['Posted']
    }, index=[1])  # Index aligns with the row in the original DataFrame to be updated

    excel_manager.update_main_dataframe(updated_df)

    # Fetch the updated DataFrame
    updated_status = excel_manager.df.loc[excel_manager.df['Post ID'] == 2, 'Status'].values[0]
    assert updated_status == 'Posted', "The Status for Post ID 2 should be updated to 'Posted'."

    # Handling NaN and empty strings equivalently for the 'Remarks' column
    excel_manager.df['Remarks'] = excel_manager.df['Remarks'].fillna('')

    # Prepare the expected DataFrame
    expected_df = pd.DataFrame({
        'Post ID': [1, 2, 3],
        'Platform': ['Instagram', 'Facebook', 'Instagram'],
        'Content': ['Check out our new product', 'New product launch', 'Product giveaway'],
        'Image Path': ['img1', 'img1', 'img1'],
        'Hashtags': ['#new #tech #insta', '#new #tech #fcbk', '#new #tech #insta'],
        'Scheduled Time': [datetime.now().date() + timedelta(days=1), datetime.now().date(),
                           datetime.now().date() - timedelta(days=1)],
        'Status': ['Scheduled', 'Posted', 'Posted'],
        'Remarks': ['', '', '']
    })

    # Convert 'Scheduled Time' in both DataFrames to date for comparison
    excel_manager.df['Scheduled Time'] = excel_manager.df['Scheduled Time'].dt.date
    expected_df['Scheduled Time'] = pd.to_datetime(expected_df['Scheduled Time']).dt.date

    # Reset index to ensure DataFrame equality check passes
    excel_manager.df.reset_index(drop=True, inplace=True)
    expected_df.reset_index(drop=True, inplace=True)

    # Use assert_frame_equal to compare the updated DataFrame against the expected DataFrame
    assert_frame_equal(excel_manager.df, expected_df, check_dtype=False, check_datetimelike_compat=True)


def test_save_changes_to_excel(excel_manager):
    """Test saving changes to the Excel file."""
    # Modify a row's Status in the dataframe
    excel_manager.df.loc[excel_manager.df['Post ID'] == 2, 'Status'] = 'Completed'
    excel_manager.save_changes_to_excel()

    # Reload the file to verify changes
    reloaded_df = pd.read_excel(excel_manager.excel_file_path)
    assert reloaded_df.loc[reloaded_df['Post ID'] == 2, 'Status'].values[0] == 'Completed'
