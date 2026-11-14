"""Extract the version number from release names."""

import re

RELEASES = ["release-2.4.1", "release-candidate"]


def version_of(name):
    match = re.search(r"(\d+\.\d+\.\d+)", name)
    return match.group(1)


def main():
    for name in RELEASES:
        print(version_of(name))


if __name__ == "__main__":
    main()
