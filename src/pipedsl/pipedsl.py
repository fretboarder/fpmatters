from typing import Callable, Generic, List, TypeVar

# Type variables
A = TypeVar("A")
B = TypeVar("B")
C = TypeVar("C")

# Type alias representing a list of lines
Lines = List[str]

# Mimicking the Unix tail command
def tail(n: int) -> Callable[[Lines], Lines]:
    """Mimicking the Unix tail command"""

    def inner(lines: Lines) -> Lines:
        return lines[-abs(n) :]  # abs -> eliminate negative input

    return inner


# Partially applied tail()
tail3 = tail(3)


def cut(d: str, f: int) -> Callable[[Lines], Lines]:
    """Mimicking the Unix cut command."""

    def field(s: str) -> str:
        try:
            splitted = s.split(d)
            return splitted[f - 1] if len(splitted) >= f else s
        except Exception:
            return str(s)

    def inner(lines: Lines) -> Lines:
        return [field(s) for s in lines]

    return inner


# Partially applied cut with delimiter ":", first field
cut_f1 = cut(d=":", f=1)


def cat(filename: str) -> Lines:
    """Mimicking the Unix cat command"""
    try:
        with open(filename) as fd:
            lines = [line for line in fd.readlines()]
        return lines
    except Exception:
        return []


def drop_comments(lines: Lines) -> Lines:
    """filter out comment lines starting with '#'."""
    return [line for line in lines if not line.startswith("#")]


# alias sort pointing to sorted
sort: Callable[[Lines], Lines] = sorted


def compose(g: Callable[[B], C], f: Callable[[A], B]) -> Callable[[A], C]:
    """Returns a new function by composing (g . f)."""
    return lambda x: g(f(x))


def last3users_imp(filename: str) -> List[str]:
    """Imperative implementation."""
    try:
        fields = []
        with open(filename) as fd:
            for line in fd.readlines():
                if not line.startswith("#"):
                    first_field = line.split(":")[0]
                    fields.append(first_field)
        return sorted(fields)[-3:]
    except Exception:
        return []


def last3users_dec(filename: str) -> List[str]:
    """Declarative implementation, functions only."""
    lines = cat(filename)
    if lines:
        return tail3(sort(cut_f1(drop_comments(lines))))
    return []


class XPipe(Generic[A]):
    """The XPipe Functor enabling shell-pipe style."""

    def __init__(self, value: A):
        self._v = value

    def __repr__(self) -> str:
        return f"XPipe[{self._v.__class__.__name__}]({self._v})"

    def map(self, func: Callable[[A], B]) -> "XPipe[B]":
        return XPipe(func(self._v))

    def __or__(self, func: Callable[[A], B]) -> "XPipe[B]":
        return self.map(func)

    @property
    def value(self) -> A:
        return self._v


def pcat(filename: str) -> XPipe[Lines]:
    """Returns the result of cat wrapped into XPipe."""
    return XPipe(cat(filename))


if __name__ == "__main__":
    lines = cat("/etc/passwd")

    result = tail(3)(sort(cut(d=":", f=1)(drop_comments(lines))))
    print("1: ", result)

    result = tail3(sort(cut_f1(drop_comments(lines))))
    print("2: ", result)

    last3 = compose(compose(tail3, sort), compose(drop_comments, cut_f1))
    result = last3(lines)
    print("3: ", result)

    presult = pcat("/etc/passwd") | drop_comments | cut(d=":", f=1) | sort | tail(3)
    print("4: ", presult)
