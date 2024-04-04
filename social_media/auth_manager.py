import json
from pathlib import Path
from typing import Dict, Optional, List
import aiofiles  # Import the aiofiles library for async file operations


class AuthManager:
    def __init__(self, credentials_file_path: Path):
        self.credentials_file_path = credentials_file_path
        # Note: We have to change how we initially load credentials since __init__ can't be async
        # We'll call load_credentials outside the __init__ to handle this.
        self.credentials = {}

    async def load_credentials(self) -> Dict[str, Dict]:
        """Load credentials from the JSON file asynchronously."""
        if not self.credentials_file_path.exists():
            raise FileNotFoundError(f"Credentials file not found: {self.credentials_file_path}")
        async with aiofiles.open(self.credentials_file_path, 'r') as file:
            content = await file.read()
            self.credentials = json.loads(content)
            return self.credentials

    def get_credentials(self, platform_name: str, user_name: str = 'default'):
        """Retrieve credentials for a specific user and platform, or the first user if 'default' or not specified."""
        platform_credentials = self.credentials.get(platform_name.lower(), [])

        # Handle 'default' user_name by returning the first user's credentials for the platform
        if user_name == 'default' or not user_name:
            return platform_credentials[0] if platform_credentials else None

        # If a specific user_name is provided, search for that user's credentials
        for user_credentials in platform_credentials:
            if user_credentials.get("user_name") == user_name:
                return user_credentials

        # If the user_name is provided but not found, you might want to handle this case, e.g., by returning None
        # or raising an exception. For simplicity, here we return None.
        return None

    async def update_credentials(self, platform_name: str, user_name: str, new_credentials: Dict):
        """Update credentials for a specific user and platform asynchronously."""
        platform_credentials = self.credentials.get(platform_name.lower(), [])
        for user_credentials in platform_credentials:
            if user_credentials.get("user_name") == user_name:
                user_credentials.update(new_credentials)
                break
        else:  # User not found, add new credentials
            platform_credentials.append({"user_name": user_name, **new_credentials})
            self.credentials[platform_name.lower()] = platform_credentials
        await self.save_credentials()  # Save asynchronously

    async def save_credentials(self):
        """Save the updated credentials back to the JSON file asynchronously."""
        async with aiofiles.open(self.credentials_file_path, 'w') as file:
            await file.write(json.dumps(self.credentials, indent=4))

    def list_users(self, platform_name: str) -> List[str]:
        """List all users for a given platform."""
        return [user_cred['user_name'] for user_cred in self.credentials.get(platform_name.lower(), [])]
