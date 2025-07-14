import sys

sys.path.insert(1, "/src/src/python")

from shopping_cart import ShoppingCart
import pytest


def test_can_add_item_to_cart():
    cart = ShoppingCart(5)
    cart.add("apple")
    assert cart.size() == 1


def test_get_items():
    cart = ShoppingCart(5)
    cart.add("apple")
    assert "apple" in cart.get_items()


def test_when_add_more_than_max_item_shold_fail():
    """_summary_"""
    cart = ShoppingCart(5)
    with pytest.raises(OverflowError):
        for _ in range(6):
            cart.add("apple")
