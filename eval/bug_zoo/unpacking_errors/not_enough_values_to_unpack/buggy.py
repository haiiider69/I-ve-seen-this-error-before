"""Split server addresses into host and port."""

ADDRESSES = ["db.internal:5432", "cache.internal"]


def split_address(address):
    host, port = address.split(":")
    return host, int(port)


def main():
    for address in ADDRESSES:
        print(split_address(address))


if __name__ == "__main__":
    main()
