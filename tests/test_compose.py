import p01.compose as cmp
import pytest


def test_compose():
    def add10(x: int) -> int:
        return x + 10

    def div2(x: int) -> float:
        return x / 2

    strid = cmp.f_after_g(f=div2, g=add10)

    assert strid(74) == 42.0
    assert cmp.f_after_g(str, strid)(74) == "42.0"
    assert cmp.f_after_g(len, cmp.f_after_g(str, strid))(74) == 4

    assert cmp.compose(div2, add10)(74) == 42.0
    assert cmp.compose(str, div2, add10)(74) == "42.0"
    assert cmp.compose(len, str, div2, add10)(74) == 4
    assert cmp.compose(cmp.compose(len, str, div2), add10)(74) == 4
    assert cmp.compose(cmp.compose(len, str), cmp.compose(div2, add10))(74) == 4
