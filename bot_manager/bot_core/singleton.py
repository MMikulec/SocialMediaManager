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
