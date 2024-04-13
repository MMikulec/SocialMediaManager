import json
import pytest
from pathlib import Path

from social_media.auth_manager.strategies.json_auth_manager import JSONAuthManager

# Sample data for use in tests
credentials_data = {
    "facebook": [{"user_name": "default", "token": "abc123", "secret": "def456"}],
    "instagram": [{"user_name": "default", "token": "xyz789", "secret": "uvw345"}]
}

credentials_json = json.dumps(credentials_data)


def test_load_credentials(monkeypatch, tmp_path):
    """Test loading of credentials from a JSON file."""
    credentials_file = tmp_path / "credentials.json"
    credentials_file.write_text(credentials_json)  # Directly using Pytest's tmp_path fixture for file handling

    """def mock_open(*args, **kwargs):
        if args[0] == str(credentials_file) and args[1] == 'r':
            return open(args[0], args[1])  # Only intercept read mode for the specific file
        else:
            open(*args, **kwargs)  # Otherwise, do not intercept

    monkeypatch.setattr("builtins.open", mock_open)  # Use monkeypatch to replace open"""

    manager = JSONAuthManager(str(credentials_file))
    assert manager.credentials == credentials_data, "The credentials should match the test data"


def test_get_credentials(tmp_path):
    """Test retrieving specific user credentials."""
    credentials_file = tmp_path / "credentials.json"
    credentials_file.write_text(credentials_json)

    manager = JSONAuthManager(str(credentials_file))
    assert manager.get_credentials("facebook") == credentials_data["facebook"][0]
    assert manager.get_credentials("facebook", "default") == credentials_data["facebook"][0]
    assert manager.get_credentials("facebook", "nonexistent") is None


def test_update_and_save_credentials(monkeypatch, tmp_path):
    """Test updating and saving credentials."""
    credentials_file = tmp_path / "credentials.json"
    credentials_file.write_text(credentials_json)

    manager = JSONAuthManager(str(credentials_file))
    new_creds = {"token": "new_token", "secret": "new_secret"}
    manager.update_credentials("facebook", "default", new_creds)

    expected_creds = credentials_data["facebook"][0].copy()
    expected_creds.update(new_creds)
    assert manager.credentials["facebook"][0] == expected_creds, "The internal credentials should be updated"

    def mock_write(file_path, data, mode='w'):
        assert file_path == str(credentials_file), "Should write to the correct file path"
        assert json.loads(data) == manager.credentials, "Should write the updated data correctly"

    monkeypatch.setattr("builtins.open", mock_write)


def test_list_users(tmp_path):
    """Test listing users for a specified platform."""
    credentials_file = tmp_path / "credentials.json"
    credentials_file.write_text(credentials_json)

    manager = JSONAuthManager(str(credentials_file))
    users = manager.list_users("facebook")
    assert users == ["default"], "Should list all usernames for the specified platform"
