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

    def get_credentials(self, platform_name: str, user_name: str) -> Optional[Dict]:
        """Retrieve credentials for a specific user and platform."""
        platform_credentials = self.credentials.get(platform_name.lower(), [])
        for user_credentials in platform_credentials:
            if user_credentials.get("user_name") == user_name:
                return user_credentials
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


import asyncio
import pprint


async def main():
    auth_manager = AuthManager(Path('../plan.json'))
    await auth_manager.load_credentials()  # Ensure credentials are loaded asynchronously
    pprint.pprint(auth_manager.get_credentials('facebook', 'user1'))  # Example usage
    # Continue with application logic...


if __name__ == "__main__":
    asyncio.run(main())
