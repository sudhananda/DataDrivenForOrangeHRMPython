class InvalidBrowserException(Exception):
    """Custom exception with a default message."""

    def __init__(self, message="Browser Name is not valid"):
        self.message = message
        super().__init__(self.message)


class FailedToEnterValueException(Exception):
    def __init__(self, message="Unable to enter value into field."):
        self.message = message
        super().__init__(self.message)


class FailedToClearValueException(Exception):
    def __init__(self, message="Unable to clear value from field."):
        self.message = message
        super().__init__(self.message)


class SelectValueFromListFailedException(Exception):
    def __init__(self, message="Unable to select value from the list as the given value is not found the list."):
        self.message = message
        super().__init__(self.message)


class TestCaseNotFoundInDataFileException(Exception):
    def __init__(self, message="Unable to select value from the list as the given value is not found the list."):
        self.message = message
        super().__init__(self.message)
