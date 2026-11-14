"""Normalize the names read from a record."""

RECORD = {"name": "Zoë Kravitz", "city": "New York"}


def clean_name(record):
    name = record.get("name")
    return name.strip().title()


def main():
    print(clean_name(RECORD))


if __name__ == "__main__":
    main()
