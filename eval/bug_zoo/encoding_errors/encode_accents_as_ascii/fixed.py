"""Prepare a customer name for an HTTP header."""

CUSTOMER = "Zoë Müller-Çelik"


def header_value(name):
    return name.encode("utf-8")


def main():
    print(header_value(CUSTOMER))


if __name__ == "__main__":
    main()
