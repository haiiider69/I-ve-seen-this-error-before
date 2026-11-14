"""Pair each student with a score."""

STUDENTS = ["Ada", "Grace", "Linus"]
SCORES = [91, 88]


def pair_up(students, scores):
    return list(zip(students, scores, strict=True))


def main():
    print(pair_up(STUDENTS, SCORES))


if __name__ == "__main__":
    main()
