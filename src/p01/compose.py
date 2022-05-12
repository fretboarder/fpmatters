import functools
from typing import Any, Callable, TypeVar

A = TypeVar("A")
B = TypeVar("B")
C = TypeVar("C")


def f_after_g(f: Callable[[B], C], g: Callable[[A], B]) -> Callable[[A], C]:
    """Compose 2 functions.add()

    Args:
        f (Callable[[B], C]): function1
        g (Callable[[A], B]): function2

    Returns:
        Callable[[A], C]: (function1 . function2)
    """

    def composed(x: A) -> C:
        return f(g(x))

    return composed


def compose(*callables: Callable[[Any], Any]) -> Callable[[Any], Any]:
    """Composes an arbitrary number of function.add()

    Returns:
        Callable[[Any], Any]: the composed function
    """
    return functools.reduce(
        lambda acc, cur: f_after_g(acc, cur), callables, lambda x: x
    )
