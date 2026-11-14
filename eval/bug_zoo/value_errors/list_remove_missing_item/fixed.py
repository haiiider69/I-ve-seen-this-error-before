"""Remove sold-out products from a shopping list."""

SHOPPING_LIST = ["milk", "eggs", "bread"]
SOLD_OUT = ["eggs", "kiwi"]


def remove_sold_out(items, sold_out):
    for product in sold_out:
        if product in items:
            items.remove(product)
    return items


def main():
    print(remove_sold_out(SHOPPING_LIST, SOLD_OUT))


if __name__ == "__main__":
    main()
