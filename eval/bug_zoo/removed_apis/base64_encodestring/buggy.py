"""Encode a small payload as base64 text."""

import base64

PAYLOAD = b"user:secret-token"


def encode(data):
    return base64.encodestring(data)


def main():
    print(encode(PAYLOAD))


if __name__ == "__main__":
    main()
