#  Copyright (c) 2024.

import pytest
import pandas as pd
from datetime import datetime, timedelta
import asyncio
from scheduler.social_media.post_executor import PostExecutor


# Parameterize the test function to accept different numbers of posts
@pytest.mark.parametrize("num_posts", [3, 5, 10, 100])  # Example: test with 3, 5, and 10 posts
def test_post_executor_start(num_posts):
    # Create a DataFrame with 'num_posts' posts
    platforms = ['Instagram', 'Facebook', 'Instagram'] * (num_posts // 3) + ['Instagram', 'Facebook', 'Instagram'][
                                                                            :num_posts % 3]
    scheduled_times = [datetime.now() + timedelta(minutes=1) for _ in range(num_posts)]

    posts_df = pd.DataFrame({
        'Post ID': range(1, num_posts + 1),
        'Platform': platforms,
        'Content': [f'Check out our new product {i}' for i in range(1, num_posts + 1)],
        'Image Path': ['img1'] * num_posts,
        'Hashtags': ['#new #tech #insta'] * num_posts,
        'Scheduled Time': scheduled_times,   # [datetime.now() + timedelta(minutes=i) for i in range(num_posts)],
        'Status': ['Scheduled'] * num_posts,
        'Remarks': [''] * num_posts,
    })

    post_executor = PostExecutor('post_executor_test.xlsx', posts_df)
    asyncio.run(post_executor.start())

    # Here you should add assertions that validate the behavior of your PostExecutor.
    # For example, you could check if the Status of all 'Scheduled' posts in DataFrame have changed to 'Posted'
    # However, for that, your PostExecutor's methods need to update the DataFrame accordingly
    # This part is left as an exercise for you as it depends on the implementation details of your PostExecutor
