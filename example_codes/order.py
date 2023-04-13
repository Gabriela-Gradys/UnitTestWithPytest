""" Methods for manipulating orders. """

from datetime import datetime, timedelta


class Status:
    """Enum for order status."""

    PENDING = "pending"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class Order:
    """ Representation of an order.

    :param prices: dictionary of items and their prices"""
    ID = 1

    def __init__(self, date: datetime, status: Status, items: [str]):
        """ Initializes order object.

        :param order_id: order id
        :param date: order date
        :param status: order status
        :param items: list of items in order
        """

        self.order_total: float = 0
        self.id = Order.ID
        Order.ID += 1

        self.date = date
        self.status = status
        self.items = items

        self.prices = {
            "pizza": 10,
            "burger": 5,
            "fries": 2,
            "coke": 1,
            "ice cream": 3,
            "salad": 4,
        }

    def calculate_total(self):
        """Calculates total price of order."""
        for item in self.items:
            self.order_total += self.prices[item]

    def expected_pickup_time(self) -> datetime:
        """Calculates waiting time for order."""
        if self.status == Status.PENDING:
            preparation_time = len(self.items) * 5
            return self.date + timedelta(minutes=preparation_time)
        else:
            return datetime.now()

    def change_order(self, items_to_delete: [str], items_to_add: [str]):
        """Changes order by adding and deleting items."""
        if self.status == Status.COMPLETED:
            raise Exception("Order is completed.")

        for item in items_to_delete:
            self.items.remove(item)
        for item in items_to_add:
            self.items.append(item)
        self.calculate_total()

    def __str__(self):
        return """This is an order {self.id} with the following items: 
        {self.items} and the total price is {self.order_total}. 
        Order status is {self.status}."""

# class ChangeOrder:
#     """Class for changing order status.
#     """
#     def __init__(self, order: Order):
