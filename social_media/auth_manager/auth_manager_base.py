# auth_manager_base.py
from abc import ABC, abstractmethod
from typing import Dict, Optional


class AbstractAuthManager(ABC):
    @abstractmethod
    async def load_credentials(self) -> Dict[str, Dict]:
        pass

    @abstractmethod
    def get_credentials(self, platform_name: str, user_name: str = 'default') -> Optional[Dict]:
        pass

    @abstractmethod
    async def update_credentials(self, platform_name: str, user_name: str, new_credentials: Dict):
        pass

    @abstractmethod
    async def save_credentials(self):
        pass
