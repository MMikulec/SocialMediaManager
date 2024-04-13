# json_auth_manager.py
from pathlib import Path
from typing import Optional, Dict, List
import json

from social_media.auth_manager.auth_manager_base import AbstractAuthManager
from social_media.auth_manager.auth_manager import AuthManager


@AuthManager.register_auth_strategy('json')
class JSONAuthManager(AbstractAuthManager):
    def __init__(self, credentials_file_path: str):
        self.credentials_file_path = credentials_file_path
        self.credentials = {}
        self.load_credentials()  # Load credentials synchronously during initialization

    def load_credentials(self) -> Dict[str, Dict]:
        """Load credentials from the JSON file synchronously."""
        if not Path(self.credentials_file_path).exists():
            raise FileNotFoundError(f"Credentials file not found: {self.credentials_file_path}")

        with open(self.credentials_file_path, 'r') as file:
            self.credentials = json.load(file)
        return self.credentials

    def get_credentials(self, platform_name: str, user_name: str = 'default') -> Optional[Dict]:
        """Retrieve credentials for a specific user and platform."""
        platform_credentials = self.credentials.get(platform_name.lower(), [])

        if user_name == 'default' or not user_name:
            return platform_credentials[0] if platform_credentials else None

        for user_credentials in platform_credentials:
            if user_credentials.get("user_name") == user_name:
                return user_credentials

        return None

    def update_credentials(self, platform_name: str, user_name: str, new_credentials: Dict):
        """Update credentials for a specific user and platform synchronously."""
        platform_credentials = self.credentials.get(platform_name.lower(), [])
        for user_credentials in platform_credentials:
            if user_credentials.get("user_name") == user_name:
                user_credentials.update(new_credentials)
                break
        else:  # User not found, add new credentials
            platform_credentials.append({"user_name": user_name, **new_credentials})
            self.credentials[platform_name.lower()] = platform_credentials

        self.save_credentials()  # Save synchronously

    def save_credentials(self):
        """Save the updated credentials back to the JSON file synchronously."""
        with open(self.credentials_file_path, 'w') as file:
            json.dump(self.credentials, file, indent=4)

    def list_users(self, platform_name: str) -> List[str]:
        """List all users for a given platform."""
        return [user_cred['user_name'] for user_cred in self.credentials.get(platform_name.lower(), [])]
