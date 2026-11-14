"""Run a background worker twice."""

import threading

RESULTS = []


def work():
    RESULTS.append("done")


def main():
    worker = threading.Thread(target=work)
    worker.start()
    worker.join()
    worker.start()
    worker.join()
    print(RESULTS)


if __name__ == "__main__":
    main()
