import threading


class PlatformBotSingleton:
    _instances = {}
    _lock = threading.Lock()

    @classmethod
    def get_instance(cls, platform_name, account_name):
        key = (platform_name, account_name)
        with cls._lock:
            if key not in cls._instances:
                instance = cls._create_instance(platform_name, account_name)
                cls._instances[key] = instance
            return cls._instances[key]

    @classmethod
    def _create_instance(cls, platform_name, account_name):
        # Placeholder for the actual instance creation logic
        # This could involve initializing a new bot instance, setting up specific configurations, etc.
        # For example:
        if platform_name == "Facebook":
            return FacebookBot(account_name)
        elif platform_name == "Instagram":
            return InstagramBot(account_name)
        else:
            raise ValueError(f"Unsupported platform: {platform_name}")


# Create or fetch the singleton instance for a specific account and platform
facebook_bot_marek = PlatformBotSingleton.get_instance("Facebook", "marek")
instagram_bot_marek = PlatformBotSingleton.get_instance("Instagram", "marek")

facebook_bot_michaela = PlatformBotSingleton.get_instance("Facebook", "michaela")
# And so on for other accounts and platforms
