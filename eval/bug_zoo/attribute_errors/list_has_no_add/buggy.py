"""Collect the distinct tags of a list of articles."""

ARTICLES = [
    {"title": "Intro", "tags": ["python", "tutorial"]},
    {"title": "Deep dive", "tags": ["python", "internals"]},
]


def distinct_tags(articles):
    seen = []
    for article in articles:
        for tag in article["tags"]:
            seen.add(tag)
    return sorted(seen)


def main():
    print(distinct_tags(ARTICLES))


if __name__ == "__main__":
    main()
