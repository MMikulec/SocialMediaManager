from dataclasses import dataclass


@dataclass
class SocialMediaPost:
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
