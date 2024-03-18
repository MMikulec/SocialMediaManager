from rich.console import Console
from rich.table import Table


def display_dataframe_as_table(dataframe, title: str):
    """Displays a pandas DataFrame as a rich table."""
    console = Console()
    table = Table(title=title)
    for column in dataframe.columns:
        table.add_column(column, justify="right", style="cyan", no_wrap=True)
    for _, row in dataframe.iterrows():
        table.add_row(*[str(value) for value in row])
    console.print(table)
