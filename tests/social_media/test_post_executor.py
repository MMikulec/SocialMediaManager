#  Copyright (c) 2024.

import pytest
import pandas as pd
from datetime import datetime, timedelta
import asyncio
from pathlib import Path
from social_media.post_executor import PostExecutor


# Parameterize the test function to accept different numbers of posts
@pytest.mark.parametrize("num_posts", [3, 5, 10, 100])  # Example: test with 3, 5, and 10 posts
def test_post_executor_start(num_posts):
    # Create a DataFrame with 'num_posts' posts
    platforms = ['Instagram', 'Facebook', 'Instagram'] * (num_posts // 3) + ['Instagram', 'Facebook', 'Instagram'][
                                                                            :num_posts % 3]
    scheduled_times = [datetime.now() + timedelta(minutes=0) for _ in range(num_posts)]

    posts_df = pd.DataFrame({
        'Post ID': range(1, num_posts + 1),
        'Platform': platforms,
        'Content': [f'Check out our new product {i}' for i in range(1, num_posts + 1)],
        'Image Path': ['img1'] * num_posts,
        'Hashtags': ['#new #tech #insta'] * num_posts,
        'Scheduled Time': scheduled_times,  # [datetime.now() + timedelta(minutes=i) for i in range(num_posts)],
        'Status': ['Scheduled'] * num_posts,
        'Remarks': [''] * num_posts,
        'User Name': ['default'] * num_posts,
    })

    post_executor = PostExecutor(Path('post_executor_test.xlsx'), posts_df)
    asyncio.run(post_executor.start())

    # Here you should add assertions that validate the behavior of your PostExecutor.
    # For example, you could check if the Status of all 'Scheduled' posts in DataFrame have changed to 'Posted'
    # However, for that, your PostExecutor's methods need to update the DataFrame accordingly
    # This part is left as an exercise for you as it depends on the implementation details of your PostExecutor


# Helper function to generate user names
def generate_user_names(num_posts, cycle_users=None):
    """
    Generate a list of user names cycling through 'cycle_users',
    repeating until reaching 'num_posts'.
    """
    if cycle_users is None:
        cycle_users = ['default', 'user1', 'user2']  # Default value is set here
    return [cycle_users[i % len(cycle_users)] for i in range(num_posts)]


@pytest.mark.parametrize("num_posts", [3, 5, 10, 100])  # Example: test with 3, 5, 10, and 100 posts
def test_post_executor_users(num_posts):
    # Generate user names including 'default' and other specific usernames
    user_names = generate_user_names(num_posts)

    # Creating a DataFrame as specified
    platforms = ['Instagram', 'Facebook', 'Instagram'] * (num_posts // 3) + ['Instagram', 'Facebook', 'Instagram'][
                                                                            :num_posts % 3]
    scheduled_times = [datetime.now() + timedelta(minutes=0) for _ in range(num_posts)]

    posts_df = pd.DataFrame({
        'Post ID': range(1, num_posts + 1),
        'Platform': platforms,
        'Content': [f'Check out our new product {i}' for i in range(1, num_posts + 1)],
        'Image Path': ['img1'] * num_posts,
        'Hashtags': ['#new #tech #insta'] * num_posts,
        'Scheduled Time': scheduled_times,
        'Status': ['Scheduled'] * num_posts,
        'Remarks': [''] * num_posts,
        'User Name': user_names
    })

    # Assuming PostExecutor's initialization and start method are correctly defined
    post_executor = PostExecutor(Path('post_executor_test.xlsx'), posts_df)
    asyncio.run(post_executor.start())
