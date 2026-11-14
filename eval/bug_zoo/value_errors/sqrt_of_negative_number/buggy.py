"""Solve a quadratic equation."""

import math


def solve_quadratic(a, b, c):
    root = math.sqrt(b * b - 4 * a * c)
    return (-b + root) / (2 * a), (-b - root) / (2 * a)


def main():
    print(solve_quadratic(1, 2, 5))


if __name__ == "__main__":
    main()
