import sys

sys.path.insert(1, "/src/src/python")
import calc
import pytest


def test_add():
    assert calc.add(10, 5) == 15

    assert calc.add(-1, 1) == 0
    assert calc.add(-1, -1) == -2


def test_subtract():
    assert calc.subtract(10, 5) == 5
    assert calc.subtract(-1, 1) == -2
    assert calc.subtract(-1, -1) == 0


def test_multiply():
    assert calc.multiply(10, 5) == 50
    assert calc.multiply(-1, 1) == -1
    assert calc.multiply(-1, -1) == 1


def test_divide():
    assert calc.divide(10, 5) == 2
    assert calc.divide(-1, 1) == -1
    assert calc.divide(-1, -1) == 1
    assert calc.divide(5, 2) == 2.5
    with pytest.raises(ValueError):
        calc.divide(10, 0)
