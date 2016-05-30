class S4Exception(Exception):
    pass


# General Exceptions

# Storage Exceptions
class StorageException(S4Exception):
    pass


class NotInS4Project(StorageException):
    '''
    Raised when attempting to perform an operation when not inside of
    an S4 project.
    '''
    pass
