"""Collect the email addresses from a CSV export."""

import csv
import io

EXPORT = "name,email\nAda,ada@example.com\nLinus,linus@example.com\n"


def emails(raw):
    reader = csv.DictReader(io.StringIO(raw))
    return [row["email"] for row in reader]


def main():
    print(emails(EXPORT))


if __name__ == "__main__":
    main()
