"""Load a settings file exported by a Windows editor."""

import json

RAW_BYTES = b"\xef\xbb\xbf" + b'{"theme": "dark", "font_size": 14}'


def load_settings(raw):
    return json.loads(raw.decode("utf-8-sig"))


def main():
    print(load_settings(RAW_BYTES))


if __name__ == "__main__":
    main()
