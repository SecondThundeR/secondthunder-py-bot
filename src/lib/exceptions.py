class CustomErrors(Exception):
    """Base class for other exceptions"""


class UsersNotFound(CustomErrors):
    """Raised when users cannot be found in database"""


class WordsImportError(CustomErrors):
    """Raised when words base imported with failure"""
