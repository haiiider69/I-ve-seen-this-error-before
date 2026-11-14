"""A tiny shopping cart."""


def add_item(cart, name, quantity=1):
    cart[name] = cart.get(name, 0) + quantity
    return cart


def main():
    cart = {}
    add_item(cart, "apples", 3)
    add_item(cart, "bread")
    print(cart)


if __name__ == "__main__":
    main()
