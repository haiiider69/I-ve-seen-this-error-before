"""Build a request for a JSON API, the Python 2 way."""

import urllib2

URL = "https://example.com/api/items"


def build_request(url):
    request = urllib2.Request(url)
    request.add_header("Accept", "application/json")
    return request


def main():
    request = build_request(URL)
    print(request.get_full_url())


if __name__ == "__main__":
    main()
