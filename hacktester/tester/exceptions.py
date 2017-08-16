class IncorrectTestFileInputError(Exception):
    pass


class FolderAlreadyExistsError(Exception):
    pass


class PollingError(Exception):
    """
    Exception raised when polling towards the Grader has failed
    """
