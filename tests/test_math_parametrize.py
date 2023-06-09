""" Tests for main.py module. """
import pytest

from example_codes.math import multiply_3


@pytest.mark.parametrize(
    "n, expected",
    [(3, 9), (2, 6), ("3", 9)]
)
def test_multiply_3(n, expected):
    """Test for multiply_3 function."""

    assert multiply_3(n) == expected
