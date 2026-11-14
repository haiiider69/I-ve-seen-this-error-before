"""Group a list of readings into fixed-size chunks."""

READINGS = [3, 5, 8, 13, 21, 34, 55]


def chunked(items, size):
    for start in range(0, len(items), size):
        yield items[start:start + size]


def main():
    for group in chunked(READINGS, 3):
        print(group)


if __name__ == "__main__":
    main()
