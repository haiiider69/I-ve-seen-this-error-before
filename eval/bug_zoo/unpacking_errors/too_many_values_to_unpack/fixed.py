"""Read people from comma-separated lines."""

LINES = ["Ada,36,London", "Linus,54,Portland"]


def parse(line):
    name, age, _city = line.split(",")
    return name, int(age)


def main():
    for line in LINES:
        print(parse(line))


if __name__ == "__main__":
    main()
