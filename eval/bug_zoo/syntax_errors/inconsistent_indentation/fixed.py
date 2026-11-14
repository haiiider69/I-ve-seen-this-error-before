"""Add up a list of prices."""


def total(prices):
    result = 0
    for price in prices:
        result += price
    return result


print(total([4, 5, 6]))
