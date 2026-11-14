"""Solve a quadratic equation."""

import math


def solve_quadratic(a, b, c):
    discriminant = b * b - 4 * a * c
    if discriminant < 0:
        return None
    root = math.sqrt(discriminant)
    return (-b + root) / (2 * a), (-b - root) / (2 * a)


def main():
    print(solve_quadratic(1, 2, 5))


if __name__ == "__main__":
    main()
