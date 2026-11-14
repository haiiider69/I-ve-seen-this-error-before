"""Run a slow helper command with a time limit."""

import subprocess
import sys

SLOW_COMMAND = [sys.executable, "-c", "import time; time.sleep(0.3); print('done')"]


def run_helper(timeout):
    result = subprocess.run(SLOW_COMMAND, capture_output=True, text=True, timeout=timeout)
    return result.stdout.strip()


def main():
    print(run_helper(timeout=0.1))


if __name__ == "__main__":
    main()
