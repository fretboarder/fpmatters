from functools import partial

from p01.compose import compose, f_after_g

soset = compose(set, sorted, list)


def test_compose():
    def add10(x: int) -> int:
        return x + 10

    def div2(x: int) -> float:
        return x / 2

    plus10div2 = f_after_g(f=div2, g=add10)

    assert plus10div2(74) == 42.0
    assert f_after_g(str, plus10div2)(74) == "42.0"
    assert f_after_g(len, f_after_g(str, plus10div2))(74) == 4

    assert compose(div2, add10)(74) == 42.0
    assert compose(str, div2, add10)(74) == "42.0"
    assert compose(len, str, div2, add10)(74) == 4
    assert compose(compose(len, str, div2), add10)(74) == 4
    assert compose(compose(len, str), compose(div2, add10))(74) == 4


def test_s_types_declarative():
    testdata = (42, (37.5,), complex(1, 1), "Python", {1, 2, 3}, {"hash": "value"})

    # create a function transforming a list of objects into a list of type names
    type_map = partial(map, lambda o: o.__class__.__name__)
    # creat a function to filter a list of strings based on the initial character
    char0_filter = lambda c: partial(filter, lambda t: t[0] == c)
    # compose both to become (char0_filter . type_map)
    s_types = compose(char0_filter("s"), type_map)
    res = s_types(testdata)
    assert soset(res) == {"set", "str"}


def test_s_types_imperative():
    def s_types(objects):
        for object in objects:
            if object.__class__.__name__[0] == "s":
                yield object.__class__.__name__

    testdata = (42, (37.5,), complex(1, 1), "Python", {1, 2, 3}, {"hash": "value"})
    res = s_types(testdata)
    assert soset(res) == {"set", "str"}
