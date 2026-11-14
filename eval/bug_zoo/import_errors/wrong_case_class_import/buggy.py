"""Report how many days are left until a deadline."""

from datetime import Datetime

DEADLINE = "2026-12-24"


def days_left(today, deadline):
    end = Datetime.strptime(deadline, "%Y-%m-%d")
    return (end - today).days


def main():
    print(days_left(Datetime(2026, 11, 11), DEADLINE))


if __name__ == "__main__":
    main()
