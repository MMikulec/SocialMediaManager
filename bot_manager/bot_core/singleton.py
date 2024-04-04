from abc import ABC


class SingletonMeta(type(ABC)):
    """
    A metaclass for creating Singleton instances. Ensures that only one instance
    of a class is created within the application context.
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            # Use 'super()' to call __call__ on the base type of ABC,
            # which bypasses ABC's checks and allows instantiation.
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class UserBasedSingletonMeta(type(ABC)):
    """
    A metaclass for creating Singleton instances based on class and user name.
    Ensures that only one instance of a class for a specific user is created
    within the application context.
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        # The user_name must be the first argument after the class (cls)
        user_name = args[0] if args else kwargs.get('user_name')
        key = (cls, user_name)
        if key not in cls._instances:
            cls._instances[key] = super().__call__(*args, **kwargs)
        return cls._instances[key]
