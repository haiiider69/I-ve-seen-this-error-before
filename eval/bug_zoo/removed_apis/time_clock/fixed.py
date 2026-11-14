"""Measure how long a computation takes."""

import time


def slow_sum(limit):
    return sum(range(limit))


def main():
    start = time.perf_counter()
    total = slow_sum(100_000)
    elapsed = time.perf_counter() - start
    print(total, elapsed >= 0)


if __name__ == "__main__":
    main()
