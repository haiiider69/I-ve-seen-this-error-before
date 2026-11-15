"""Tests for building the evaluation memory from the bug zoo."""

import json
from collections.abc import Iterator
from pathlib import Path

import pytest

from steb.store.database import ErrorStore
from steb.zoo import Bug, load_bug
from steb.zoo_memory import MemoryBuildError, build_memory, script_name_for

DIVIDE = (
    '"""Divide two numbers."""\n\n\n'
    "def divide(a, b):\n    return a / b\n\n\n"
    "print(divide(1, 0))\n"
)
LOOKUP = '"""Divide two numbers."""\n\nDATA = {}\nprint(DATA["missing"])\n'
SILENT_FAILURE = 'import sys\nprint("boom")\nsys.exit(1)\n'


def make_bug(root: Path, slug: str, buggy: str, fix_summary: str = "Check the input.") -> Bug:
    """Create a bug folder in a temporary zoo and load it."""
    folder = root / "value_errors" / slug
    folder.mkdir(parents=True)
    (folder / "buggy.py").write_text(buggy, encoding="utf-8")
    (folder / "fixed.py").write_text("print('fixed')\n", encoding="utf-8")
    meta = {
        "id": f"value_errors/{slug}",
        "category": "value_errors",
        "title": f"Bug {slug}",
        "exception": "ZeroDivisionError",
        "message_contains": "division",
        "fix_summary": fix_summary,
    }
    (folder / "meta.json").write_text(json.dumps(meta), encoding="utf-8")
    return load_bug(folder)


@pytest.fixture
def store() -> Iterator[ErrorStore]:
    with ErrorStore(":memory:") as opened:
        yield opened


@pytest.mark.parametrize(
    ("source", "expected"),
    [
        ('"""Build a database connection string."""\n', "build_database.py"),
        ('"""Report how many days are left until a deadline."""\n', "report_days.py"),
        ('"""A tiny shopping cart."""\n', "tiny_shopping.py"),
        ('"""Divide."""\n', "divide.py"),
        ("print('no docstring')\n", "script.py"),
        ('"""The of a."""\n', "script.py"),
        ("", "script.py"),
    ],
)
def test_script_name_comes_from_the_docstring(source: str, expected: str) -> None:
    assert script_name_for(source) == expected


def test_a_bug_is_recorded_with_its_fix(tmp_path: Path, store: ErrorStore) -> None:
    bug = make_bug(tmp_path / "zoo", "divide_by_zero", DIVIDE, fix_summary="Check the divisor.")
    entries = build_memory([bug], store)

    assert len(entries) == 1
    entry = entries[0]
    assert entry.bug_id == "value_errors/divide_by_zero"
    assert entry.script == "divide_two.py"

    stored = store.get_error(entry.error_id)
    assert stored is not None
    assert stored.exc_type == "ZeroDivisionError"
    assert stored.fingerprint == entry.fingerprint
    assert "divide_two.py" in stored.normalized_text
    assert "buggy.py" not in stored.normalized_text
    assert [fix.note for fix in store.fixes_for(entry.error_id)] == ["Check the divisor."]

    occurrence = store.occurrences_for(entry.error_id)[0]
    assert occurrence.language == "python"
    assert occurrence.command is not None
    assert "divide_two.py" in occurrence.command


def test_each_bug_gets_its_own_record_and_script_name(tmp_path: Path, store: ErrorStore) -> None:
    zoo = tmp_path / "zoo"
    bugs = [make_bug(zoo, "first", DIVIDE), make_bug(zoo, "second", LOOKUP)]
    entries = build_memory(bugs, store)

    assert [entry.bug_id for entry in entries] == [bug.id for bug in bugs]
    assert [entry.script for entry in entries] == ["divide_two.py", "divide_two_2.py"]
    assert len({entry.error_id for entry in entries}) == 2
    assert len({entry.fingerprint for entry in entries}) == 2
    assert len(store.list_errors()) == 2


def test_error_ids_follow_the_bug_order(tmp_path: Path, store: ErrorStore) -> None:
    zoo = tmp_path / "zoo"
    bugs = [make_bug(zoo, "first", DIVIDE), make_bug(zoo, "second", LOOKUP)]
    entries = build_memory(bugs, store)
    assert [entry.error_id for entry in entries] == [1, 2]


def test_bugs_with_the_same_fingerprint_are_reported(tmp_path: Path, store: ErrorStore) -> None:
    zoo = tmp_path / "zoo"
    bugs = [make_bug(zoo, "one", SILENT_FAILURE), make_bug(zoo, "two", SILENT_FAILURE)]
    with pytest.raises(MemoryBuildError, match="value_errors/two.*value_errors/one"):
        build_memory(bugs, store)


def test_a_bug_that_does_not_fail_is_reported(tmp_path: Path, store: ErrorStore) -> None:
    bug = make_bug(tmp_path / "zoo", "fine", "print('all good')\n")
    with pytest.raises(MemoryBuildError, match="no error was recorded"):
        build_memory([bug], store)


def test_an_explicit_working_directory_is_used(tmp_path: Path, store: ErrorStore) -> None:
    bug = make_bug(tmp_path / "zoo", "divide_by_zero", DIVIDE)
    workdir = tmp_path / "work"
    workdir.mkdir()
    build_memory([bug], store, workdir=workdir)
    assert (workdir / "divide_two.py").is_file()
