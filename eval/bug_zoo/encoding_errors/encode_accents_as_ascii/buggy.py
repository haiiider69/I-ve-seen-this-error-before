"""Prepare a customer name for an HTTP header."""

CUSTOMER = "Zoë Müller-Çelik"


def header_value(name):
    return name.encode("ascii")


def main():
    print(header_value(CUSTOMER))


if __name__ == "__main__":
    main()
