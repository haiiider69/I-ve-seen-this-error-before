"""Print a short report of order totals."""

ORDERS = [12.5, 7.25, 30.0]


def report(orders):
    print("orders:", len(orders))
    print("total:", sum(orders))


report(ORDERS)
