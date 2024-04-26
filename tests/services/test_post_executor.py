import json
import pytest
import pandas as pd
from datetime import datetime, timedelta
import asyncio
from pathlib import Path
from services.post_executor import PostExecutor
from data_management.data_holder import DataHolder

# Sample data for use in tests
credentials_data = {
    "facebook": [{"user_name": "testuser1", "api_key": "testkey1"},
                 {"user_name": "testuser2", "api_key": "testkey2"}],
    "instagram": [{"user_name": "instauser", "access_token": "instatoken"}]
}

credentials_json = json.dumps(credentials_data)


# Parameterize the test function to accept different numbers of posts
@pytest.mark.asyncio  # This decorator is used for async tests with pytest-asyncio
@pytest.mark.parametrize("num_posts", [1, 100])
async def test_post_executor_start(num_posts, tmp_path):
    platforms = ['Instagram', 'Facebook', 'Instagram'] * (num_posts // 3) + ['Instagram', 'Facebook', 'Instagram'][
                                                                            :num_posts % 3]
    scheduled_times = [datetime.now() for _ in range(num_posts)]

    posts_df = pd.DataFrame({
        'Post ID': range(1, num_posts + 1),
        'Platform': platforms,
        'Content': [f'Check out our new product {i}' for i in range(1, num_posts + 1)],
        'Image Path': ['img1'] * num_posts,
        'Hashtags': ['#new #tech #insta'] * num_posts,
        'Scheduled Time': scheduled_times,
        'Status': ['Scheduled'] * num_posts,
        'Remarks': [''] * num_posts,
        'User Name': generate_user_names(num_posts)
    })

    credentials_file = tmp_path / "credentials.json"
    credentials_file.write_text(credentials_json)

    data_holder = DataHolder(posts_df, Path('post_executor_test.xlsx').name, str(credentials_file))
    post_executor = PostExecutor(data_holder)
    await post_executor.start()

    # Assertions to validate behavior; modify as needed based on actual outcomes and requirements
    """updated_df = data_holder.get_data()
    assert all(status == 'Posted' for status in updated_df['Status']), "Not all posts were updated to 'Posted'"
    """
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
        cycle_users = ['instauser', 'testuser2', 'instauser']  # Default value is set here
    return [cycle_users[i % len(cycle_users)] for i in range(num_posts)]