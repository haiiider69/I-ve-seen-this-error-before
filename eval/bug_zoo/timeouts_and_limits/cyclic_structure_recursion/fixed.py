"""Compute how many levels an organisation chart has."""

CEO = {"name": "ceo", "reports": []}
CTO = {"name": "cto", "reports": []}
CEO["reports"].append(CTO)


def depth(person):
    deepest = 0
    for report in person["reports"]:
        deepest = max(deepest, depth(report))
    return 1 + deepest


def main():
    print(depth(CEO))


if __name__ == "__main__":
    main()
