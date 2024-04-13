from datetime import datetime
import re

import pandas as pd
from rich.console import Console
from rich.table import Table
from logger_config import logger, console


class DataHolder:
    """
    A simple class to hold and provide access to a pandas DataFrame throughout
    the application, ensuring that updates to the DataFrame are reflected
    wherever the DataHolder is accessed.
    """

    # TODO: 11. 4. 2024: New variable for data source. It can replace file_path!
    def __init__(self, dataframe: pd.DataFrame, data_source=None, credential_source=None):
        self.dataframe = dataframe
        self.data_source = data_source
        self.credential_source = credential_source

        # Define column names as attributes
        self.post_id_column = "Post ID"
        self.platform_column = "Platform"
        self.content_column = "Content"
        self.image_path_column = "Image Path"
        self.hashtags_column = "Hashtags"
        self.scheduled_time_column = "Scheduled Time"
        self.status_column = "Status"
        self.user_name_column = "User Name"

        self.validate_data()

    def validate_data(self):
        """Validates the DataFrame for mandatory columns, unique, and non-empty constraints."""
        self.check_mandatory_columns()
        self.check_unique_conditions()
        self.check_non_empty_conditions()

    def check_mandatory_columns(self):
        """
        Ensures all predefined columns are present in the DataFrame.

        Raises:
        ValueError: If any mandatory column is missing.
        """
        mandatory_columns = [
            self.post_id_column, self.platform_column, self.content_column,
            self.image_path_column, self.hashtags_column, self.scheduled_time_column,
            self.status_column, self.user_name_column
        ]

        missing_columns = [col for col in mandatory_columns if col not in self.dataframe.columns]
        if missing_columns:
            raise ValueError(f"Missing mandatory columns: {', '.join(missing_columns)}")

    def check_unique_conditions(self):
        """
        Ensures that values in the 'Post ID' column are unique.

        Raises:
        ValueError: If 'Post ID' values are not unique.
        """
        if self.dataframe[self.post_id_column].duplicated().any():
            raise ValueError(f"Values in column '{self.post_id_column}' must be unique.")

    def check_non_empty_conditions(self):
        """
        Ensures that certain columns do not contain empty values.

        Raises:
        ValueError: If specified columns contain empty values.
        """
        non_empty_columns = [self.user_name_column]  # Add more columns if needed

        for column in non_empty_columns:
            if self.dataframe[column].isnull().any() or self.dataframe[column].eq('').any():
                raise ValueError(f"Column '{column}' cannot contain empty values.")

    def get_data(self):
        """
        Returns the contained DataFrame.
        """
        return self.dataframe

    def set_data(self, new_dataframe):
        """
        Replaces the current DataFrame with a new one.

        :param new_dataframe: The new DataFrame to replace the old one.
        """
        self.dataframe = new_dataframe

    def update_data(self, new_data):
        """
        Updates the DataFrame with new data. This method can be tailored to handle
        different types of updates depending on how `new_data` is structured.

        :param new_data: The new DataFrame to replace the old one.
        """
        self.dataframe.update(new_data)

    def load_current_date_posts(self):
        try:
            current_date = datetime.now().date()
            return self.dataframe[self.dataframe[self.scheduled_time_column].dt.date == current_date]
        except Exception as e:
            print(f"Error loading current date posts: {e}")
            return pd.DataFrame()

    @staticmethod
    def check_credentials_source(source):
        # Regular expression to match a string ending with a file extension
        file_match = re.search(r'\.([a-zA-Z0-9]+)$', source)

        if file_match:
            logger.info(f"It's a file with extension {file_match.group(1)}")
            return file_match.group(1)

        # Check for a pattern that might represent a database connection string
        elif re.search(r'^\w+:\/\/', source):
            logger.info(f"It's a database connection string")
            return "database"

        # Default case if the source is neither recognized as a file nor as a database connection string
        else:
            raise ValueError("The source type is unknown or not supported.")

    @staticmethod
    def display_dataframe_as_table(dataframe: pd.DataFrame, title: str):
        """
        Displays a pandas DataFrame as a rich table.

        :param dataframe: The DataFrame to display.
        :param title: The title of the table.
        """
        console = Console()
        table = Table(title=title)

        for column in dataframe.columns:
            table.add_column(column, justify="right", style="cyan", no_wrap=True)
        for _, row in dataframe.iterrows():
            table.add_row(*[str(value) for value in row])

        console.print(table)
