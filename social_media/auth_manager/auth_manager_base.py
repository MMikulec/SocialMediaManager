from abc import ABC, abstractmethod

from typing import Protocol, Dict, Optional, runtime_checkable


@runtime_checkable
class AuthManagerProtocol(Protocol):
    def load_credentials(self) -> Dict[str, Dict]: ...

    def get_credentials(self, platform_name: str, user_name: str = 'default') -> Optional[Dict]: ...

    def update_credentials(self, platform_name: str, user_name: str, new_credentials: Dict): ...

    def save_credentials(self): ...


class AbstractAuthManager(ABC):
    @abstractmethod
    def load_credentials(self) -> Dict[str, Dict]:
        """
        Load credentials and return them as a dictionary.
        This method should be implemented to handle the loading of credentials from a storage system.
        """
        pass

    @abstractmethod
    def get_credentials(self, platform_name: str, user_name: str = 'default') -> Optional[Dict]:
        """
        Retrieve credentials for a specific platform and user. Defaults to 'default' user if not specified.

        :param platform_name: The name of the platform for which to retrieve credentials.
        :param user_name: The username for whom to retrieve credentials.
        :return: A dictionary of credentials if available, otherwise None.
        """
        pass

    @abstractmethod
    def update_credentials(self, platform_name: str, user_name: str, new_credentials: Dict):
        """
        Update credentials for a specific platform and user.

        :param platform_name: The name of the platform for which to update credentials.
        :param user_name: The username for whom to update credentials.
        :param new_credentials: A dictionary containing the new credentials.
        """
        pass

    @abstractmethod
    def save_credentials(self):
        """
        Save credentials asynchronously. This method should implement the logic to save
        the updated credentials to a storage system.
        """
        pass
