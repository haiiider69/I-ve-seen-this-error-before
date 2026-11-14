"""Group a list of readings into fixed-size chunks."""

from .chunking import chunked

READINGS = [3, 5, 8, 13, 21, 34, 55]


def main():
    for group in chunked(READINGS, 3):
        print(group)


if __name__ == "__main__":
    main()
