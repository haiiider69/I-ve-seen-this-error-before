"""Back up a notes file."""

import os
import shutil
import tempfile


def main():
    with tempfile.TemporaryDirectory() as folder:
        source = os.path.join(folder, "note.txt")
        with open(source, "w", encoding="utf-8") as handle:
            handle.write("buy milk")
        shutil.copy(source, os.path.join(folder, "notes.bak"))
        print("backup done")


if __name__ == "__main__":
    main()
