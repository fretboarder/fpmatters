from typing import Callable

from p01.compose import f_after_g


def typename(obj: object) -> str:
    """Get typename of object.

    Args:
        obj (object): an arbitrary python object

    Returns:
        str: the type name of the object
    """
    return obj.__class__.__name__


def uppercase(s: str) -> str:
    """Convert a string to uppercase.

    Args:
        s (str): an arbitrary string

    Returns:
        str: a new uppercase string
    """
    return s.upper()


uppertype: Callable[[object], str] = f_after_g(uppercase, typename)
