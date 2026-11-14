"""Pair each student with a score."""

from itertools import zip_longest

STUDENTS = ["Ada", "Grace", "Linus"]
SCORES = [91, 88]


def pair_up(students, scores):
    return list(zip_longest(students, scores, fillvalue=0))


def main():
    print(pair_up(STUDENTS, SCORES))


if __name__ == "__main__":
    main()
