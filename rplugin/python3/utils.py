from enum import Enum


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
