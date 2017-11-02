"""
    Errors for use in the pi stack daemon
    Philip Basford
    November 2017
"""

class StackError(Exception):
    """
        Top level error for al pistack related issues
    """
    pass

class NoStackFound(StackError):
    """
        No pistack found when checking HAT ID
    """
    pass
