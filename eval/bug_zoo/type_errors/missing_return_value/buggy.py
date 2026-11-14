"""Parse 'x,y' coordinates from text."""


def parse_point(text):
    x, y = text.split(",")
    point = (float(x), float(y))


def main():
    first = parse_point("3.5,4.25")
    print(first[0])


if __name__ == "__main__":
    main()
