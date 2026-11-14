"""List the parameter names of a function."""

import inspect


def connect(host, port, timeout=5):
    return f"{host}:{port}"


def parameter_names(func):
    return inspect.getfullargspec(func).args


def main():
    print(parameter_names(connect))


if __name__ == "__main__":
    main()
