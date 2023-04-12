""" Tests for main.py module. """
import pytest

from example_codes.math import do_math, multiply_3

# Input: 2, output: 6


@pytest.mark.parametrize("n, expected", [(2, 6), (4, 12), (5, 15), (4,8)])
def test_do_math(n, expected):
    """Test for do_math function."""
    # 2 * 2 + 2
    # 2 + 2 + 2
    # 2 * 3
    # 2 * 4 - 2
    assert do_math(n) == expected


def test_multiply_3():
    """Test for multiply_3 function."""

    assert multiply_3(2) == 6
    assert multiply_3(3) == 9
