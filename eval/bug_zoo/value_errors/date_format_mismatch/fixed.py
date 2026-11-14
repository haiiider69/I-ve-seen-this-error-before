"""Compute the age of an invoice in days."""

from datetime import date, datetime

INVOICE_DATE = "11/05/2026"


def invoice_age(raw, today):
    issued = datetime.strptime(raw, "%m/%d/%Y").date()
    return (today - issued).days


def main():
    print(invoice_age(INVOICE_DATE, date(2026, 11, 11)))


if __name__ == "__main__":
    main()
