import json
from data_management.auth_manager.auth_manager import AuthManager
from data_management.auth_manager.auth_manager_base import AuthManagerProtocol

CREDENTIALS_FILE = r"data_management/auth_manager/test_credentials.json"

# Sample data for use in tests
credentials_data = {
        "facebook": [{"user_name": "testuser1", "api_key": "testkey1"},
                     {"user_name": "testuser2", "api_key": "testkey2"}],
        "instagram": [{"user_name": "instauser", "access_token": "instatoken"}]
    }

credentials_json = json.dumps(credentials_data)


def test_auth_manager(tmp_path):
    credentials_file = tmp_path / "credentials.json"
    credentials_file.write_text(credentials_json)

    auth_manager = AuthManager()
    credentials_type = "json"
    strategy_instance = auth_manager.get_strategy_instance(credentials_type, credentials_file)

    credentials = strategy_instance.get_credentials("facebook", "testuser1")

    assert strategy_instance is not None
    assert "facebook" in strategy_instance.credentials
    assert "instagram" in strategy_instance.credentials

    assert credentials["api_key"] == "testkey1"

    assert isinstance(strategy_instance, AuthManagerProtocol)
