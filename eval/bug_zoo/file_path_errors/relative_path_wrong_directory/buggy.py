"""Write a settings file, then read it back."""

import os
import tempfile


def write_settings(folder):
    path = os.path.join(folder, "settings.ini")
    with open(path, "w", encoding="utf-8") as handle:
        handle.write("[app]\nname = demo\n")
    return path


def read_settings(path):
    with open(path, encoding="utf-8") as handle:
        return handle.read()


def main():
    with tempfile.TemporaryDirectory() as folder:
        write_settings(folder)
        print(read_settings("settings.ini"))


if __name__ == "__main__":
    main()
