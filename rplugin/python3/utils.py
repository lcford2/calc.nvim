from enum import Enum
from datetime import datetime

class LogLevel(Enum):
    """LogLevel enum for level checking and comparisons."""

    TRACE = 0
    DEBUG = 1
    INFO = 2
    WARN = 3
    ERROR = 4
    FATAL = 5

    def __gt__(self, other):
        """Provide ability to use ">" to check greater than for log levels.

        Compares the valus of the enum elements.

        Args:
            other (LogLevel): Other LogLevel element to compare against.
        """
        return self.value > other.value

    def __lt__(self, other):
        """Provide ability to use "<" to check less than for log levels.

        Compares the valus of the enum elements.

        Args:
            other (LogLevel): Other LogLevel element to compare against.
        """
        return self.value < other.value

    def __ge__(self, other):
        """Provide ability to use ">=" to check greater than or equal to for log levels.

        Compares the valus of the enum elements.

        Args:
            other (LogLevel): Other LogLevel element to compare against.
        """
        return self.value >= other.value

    def __le__(self, other):
        """Provide ability to use "<=" to check less than or equal to for log levels.

        Compares the valus of the enum elements.

        Args:
            other (LogLevel): Other LogLevel element to compare against.
        """
        return self.value <= other.value


def strings_to_ints(strings: list[str]) -> list[int]:
    """Convert a list of strings to a list of integers.

    Args:
        strings (list[str]): List of strings that can be converted to integers

    Returns:
        list[int]: List of integers from the strings provided
    """
    return [int(i) for i in strings]

def get_timestamp(dt=None):
    """Get the isoformatted timestamp.

    If dt is not provided, will return the current time.

    Args:
        dt (datetime, optional): A datetime to convert to isoformat
    """
    if dt:
        return datetime.isoformat(dt)
    else:
        return datetime.isoformat(datetime.now())
