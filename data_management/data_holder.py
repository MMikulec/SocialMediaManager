from datetime import datetime

import pandas as pd
from rich.console import Console
from rich.table import Table


class DataHolder:
    """
    A simple class to hold and provide access to a pandas DataFrame throughout
    the application, ensuring that updates to the DataFrame are reflected
    wherever the DataHolder is accessed.
    """

    # TODO: 11. 4. 2024: New variable for data source. It can replace file_path!
    def __init__(self, dataframe: pd.DataFrame, data_source=None):
        self.dataframe = dataframe
        self.data_source = data_source
        self.date_column = 'Scheduled Time'

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
            return self.dataframe[self.dataframe[self.date_column].dt.date == current_date]
        except Exception as e:
            print(f"Error loading current date posts: {e}")
            return pd.DataFrame()

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
