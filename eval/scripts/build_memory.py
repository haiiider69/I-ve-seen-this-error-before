"""Build the evaluation memory: run every bug of the zoo through steb and record its fix.

Run from the repository root:

    uv run python eval/scripts/build_memory.py

This creates a separate database (``data/eval/zoo_memory.db`` by default, never your personal
one) and a JSON file next to it that links each bug to its record. Use ``--overwrite`` to rebuild
an existing database.
"""

import argparse
import json
import sys
from pathlib import Path

from steb.store.database import ErrorStore
from steb.zoo import load_zoo
from steb.zoo_memory import MemoryBuildError, build_memory

DEFAULT_OUT = Path("data/eval/zoo_memory.db")


def main(argv: list[str] | None = None) -> int:
    """Build the zoo memory and its bug-to-record map.

    Args:
        argv: Command-line arguments (defaults to ``sys.argv``).

    Returns:
        0 on success, 1 if a bug could not be recorded, 2 on a usage problem.
    """
    parser = argparse.ArgumentParser(description="Build the evaluation memory from the bug zoo.")
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT, help="database file to create")
    parser.add_argument("--overwrite", action="store_true", help="replace an existing database")
    args = parser.parse_args(argv)

    database: Path = args.out
    if database.exists():
        if not args.overwrite:
            print(f"error: {database} already exists (use --overwrite to rebuild it)")
            return 2
        database.unlink()

    bugs = load_zoo()
    print(f"Running {len(bugs)} bugs through steb...")
    try:
        with ErrorStore(database) as store:
            entries = build_memory(bugs, store)
    except MemoryBuildError as exc:
        database.unlink(missing_ok=True)
        print(f"error: {exc}")
        return 1

    link_file = database.with_suffix(".json")
    links = {
        entry.bug_id: {
            "error_id": entry.error_id,
            "fingerprint": entry.fingerprint,
            "script": entry.script,
        }
        for entry in entries
    }
    link_file.write_text(json.dumps({"database": database.name, "bugs": links}, indent=2) + "\n")

    for entry in entries:
        print(f"  #{entry.error_id:<3} {entry.fingerprint}  {entry.script:<28} {entry.bug_id}")
    print(f"\n{len(entries)} errors and fixes recorded in {database}")
    print(f"bug-to-record map written to {link_file}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
