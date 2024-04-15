from dataclasses import dataclass
import pandas as pd


@dataclass
class MediaContent:
    """
    Represents a post to be shared on social media platforms.

    Attributes:
        post_id (int): Unique identifier for the post, typically sourced from an Excel file.
        content (str): The text content of the social media post.
        image_path (str): File path to an image associated with the post, if any.
        hashtags (str): A string of hashtags to include in the post.
    """
    post_id: int  # Unique identifier for the post from Excel
    content: str
    image_path: str
    hashtags: str

    @classmethod
    def from_dataframe_row(cls, row: pd.Series) -> 'MediaContent':
        """
        Converts a row from a DataFrame into a MediaContent object.

        :param row: A pandas Series object representing the data for a single post.
        :return: A MediaContent object populated with the data from the row.
        """
        return cls(
            post_id=row['Post ID'],
            content=row['Content'],
            image_path=row['Image Path'],
            hashtags=row['Hashtags']
        )
