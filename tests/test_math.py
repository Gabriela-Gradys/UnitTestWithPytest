""" Tests for main.py module. """
import pytest

from example_codes.math import multiply_3


def test_multiply_3():
    """Test for multiply_3 function.

    multiply_3 takes n (int/str) and returns n * 3 """

    assert multiply_3(3) == 9
    # assert multiply_3(2) == 6
    # assert multiply_3("3") == 9
