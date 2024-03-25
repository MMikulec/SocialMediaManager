import pytest
import aiofiles
import json
from pathlib import Path
from social_media.auth_manager import AuthManager  # Correct this import as needed


@pytest.fixture
async def temp_credentials_file(tmp_path):
    """Create a temporary JSON file for testing asynchronously."""
    credentials = {
        "facebook": [{"user_name": "testuser1", "api_key": "testkey1"},
                     {"user_name": "testuser2", "api_key": "testkey2"}],
        "instagram": [{"user_name": "instauser", "access_token": "instatoken"}]
    }
    file_path = tmp_path / "test_credentials.json"
    async with aiofiles.open(file_path, 'w') as f:
        await f.write(json.dumps(credentials))
    return file_path  # Return the path object directly, not as a coroutine


# Asynchronous test for load_credentials
# Correcting the asynchronous tests
@pytest.mark.asyncio
async def test_load_credentials(temp_credentials_file):
    auth_manager = AuthManager(await temp_credentials_file)  # Corrected
    await auth_manager.load_credentials()  # Await the async method
    assert "facebook" in auth_manager.credentials
    assert "instagram" in auth_manager.credentials
    assert auth_manager.credentials["facebook"][0]["api_key"] == "testkey1"


@pytest.mark.asyncio
async def test_get_credentials(temp_credentials_file):
    auth_manager = AuthManager(await temp_credentials_file)  # Corrected
    await auth_manager.load_credentials()  # Await async method before testing
    credentials = auth_manager.get_credentials("facebook", "testuser1")
    assert credentials["api_key"] == "testkey1"


@pytest.mark.asyncio
async def test_update_credentials(temp_credentials_file):
    auth_manager = AuthManager(await temp_credentials_file)  # Corrected
    await auth_manager.load_credentials()  # Await async method before testing
    new_credentials = {"api_key": "newtestkey"}
    await auth_manager.update_credentials("facebook", "testuser1", new_credentials)
    updated_credentials = auth_manager.get_credentials("facebook", "testuser1")
    assert updated_credentials["api_key"] == "newtestkey"


# Synchronous test for list_users
@pytest.mark.asyncio
async def test_list_users(temp_credentials_file):
    auth_manager = AuthManager(await temp_credentials_file)
    await auth_manager.load_credentials()  # Await async method before testing
    users = auth_manager.list_users("facebook")
    assert "testuser1" in users
    assert "testuser2" in users
