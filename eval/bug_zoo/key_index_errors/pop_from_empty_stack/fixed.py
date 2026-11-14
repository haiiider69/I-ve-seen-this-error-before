"""Check that brackets in a string are balanced."""

PAIRS = {")": "(", "]": "[", "}": "{"}


def is_balanced(text):
    stack = []
    for char in text:
        if char in "([{":
            stack.append(char)
        elif char in PAIRS:
            if not stack or stack.pop() != PAIRS[char]:
                return False
    return not stack


def main():
    print(is_balanced("(a[b]c)"))
    print(is_balanced("a)b("))


if __name__ == "__main__":
    main()
