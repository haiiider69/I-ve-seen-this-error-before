"""Print a numbered list of names."""

NAMES = ["Ada", "Grace", "Linus"]


def numbered(names):
    lines = []
    for index in range(len(names) + 1):
        lines.append(f"{index + 1}. {names[index]}")
    return lines


def main():
    for line in numbered(NAMES):
        print(line)


if __name__ == "__main__":
    main()
