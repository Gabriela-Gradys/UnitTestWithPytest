""" Tests for main.py module. """
import pytest

from example_codes.math import do_math, multiply_3


# Input: 2, output: 6
def test_do_math():
    """Test for do_math function."""
    # 2 * 2 + 2
    # 2 + 2 + 2
    # 2 * 3
    # 2 * 4 - 2
    assert do_math(2) == 6
    assert do_math(4) == 12


def test_multiply_3():
    """Test for multiply_3 function."""

    assert multiply_3(2) == 6
    assert multiply_3(3) == 9
