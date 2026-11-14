"""Sum the quantities of an order given as text."""

ORDER = "2, 5, 3.5, 1"


def total_quantity(text):
    return sum(int(part) for part in text.split(","))


def main():
    print(total_quantity(ORDER))


if __name__ == "__main__":
    main()
