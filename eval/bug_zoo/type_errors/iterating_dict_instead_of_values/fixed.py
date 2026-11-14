"""Print the names of configured services."""

SERVICES = {
    "web": {"name": "frontend", "port": 8000},
    "db": {"name": "postgres", "port": 5432},
}


def service_names(services):
    return [entry["name"] for entry in services.values()]


def main():
    print(service_names(SERVICES))


if __name__ == "__main__":
    main()
