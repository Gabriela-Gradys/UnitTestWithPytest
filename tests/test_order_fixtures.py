""" Test order module with fixtures. """
import time
from datetime import datetime, timedelta

import pytest

from example_codes.order import Order, Status


@pytest.fixture
def test_order(test_date, request):
    order = Order(
        date=test_date,
        status=Status.PENDING,
        items=request.param
    )
    return order


@pytest.fixture()
def test_date():
    return datetime.now()


@pytest.mark.parametrize("test_order, expected", [
    (["pizza", "burger", "fries", "coke", "ice cream", "salad"], 25),
    (["pizza", "fries", "salad"], 16),
    (["burger", "coke"], 6),
], indirect=["test_order"])
def test_order_total(test_order, expected):
    test_order.calculate_total()
    assert test_order.order_total == expected


@pytest.mark.orders
def test_expected_pickup_time(test_order):
    expected_time = test_order.expected_pickup_time()
    assert expected_time == datetime.now() + timedelta(minutes=30)
    # assert expected_time == test_date + timedelta(minutes=30)


@pytest.mark.orders
def test_change_order(test_order):
    test_order.change_order(items_to_delete=["pizza", "burger"],
                            items_to_add=["salad"])
    assert test_order.items == ["fries", "coke", "ice cream", "salad", "salad"]
    assert test_order.order_total == 14


@pytest.mark.orders
def test_change_completed_order(test_order):
    test_order.status = Status.COMPLETED
    with pytest.raises(Exception,  match="Order is completed."):
        test_order.change_order(items_to_delete=["pizza"],
                                items_to_add=["salad"])

# Testy klasy Status


@pytest.mark.status
def test_status():
    assert Status.PENDING == "pending"
    assert Status.COMPLETED == "completed"
    assert Status.CANCELLED == "cancelled"
