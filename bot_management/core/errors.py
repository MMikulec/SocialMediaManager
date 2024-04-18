class CredentialError(Exception):
    """Exception raised for errors in the authentication process.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message="Credentials are invalid or expired"):
        self.message = message
        super().__init__(self.message)
