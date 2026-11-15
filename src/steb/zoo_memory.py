"""Zoo memory: fill an error store with the bug zoo, the way a real user would.

Every bug's ``buggy.py`` is run through the real capture code (``run_and_capture``), so the error
goes through exactly the path of ``steb run``: extraction, redaction, normalization, fingerprinting
and storage. The reference fix is then recorded like ``steb fix`` would.

Each script is run under a realistic file name taken from its docstring (``report_days.py``) and
not under ``buggy.py``: real tracebacks do not all show the same file name, and a name that
described the bug would leak the answer into the error text.

The result links every bug to its record in the store. That link is the ground truth for the
evaluation: a search for a bug's error must lead back to that record.
"""

import re
import sys
import tempfile
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path

from steb.capture.runner import run_and_capture
from steb.store.database import ErrorStore
from steb.zoo import Bug

_STOPWORDS = frozenset(
    {
        "a", "an", "the", "of", "to", "from", "in", "on", "for", "and", "or", "with", "by",
        "how", "many", "is", "are", "that", "this", "into", "at", "as", "it", "its", "be",
        "some", "each", "every", "all",
    }
)
_DEFAULT_NAME = "script"
_NAME_WORDS = 2


class MemoryBuildError(RuntimeError):
    """Raised when a bug cannot be turned into exactly one record of the memory."""


@dataclass(frozen=True, slots=True)
class MemoryEntry:
    """The link between a zoo bug and its record in the store.

    Attributes:
        bug_id: The bug's identifier (``<category>/<slug>``).
        error_id: The id of the bug's record in the store.
        fingerprint: The fingerprint of the recorded error.
        script: The file name the script was run under.
    """

    bug_id: str
    error_id: int
    fingerprint: str
    script: str


def script_name_for(source: str) -> str:
    """Choose a realistic file name for a script, from the first line of its docstring.

    Args:
        source: The script's source code.

    Returns:
        A name such as ``report_days.py`` (``script.py`` if the docstring has no usable words).
    """
    match = re.match(r'\s*"""([^\n]*?)(?:"""|$)', source)
    words = re.findall(r"[a-z]+", match.group(1).lower()) if match else []
    kept = [word for word in words if word not in _STOPWORDS][:_NAME_WORDS]
    return f"{'_'.join(kept) if kept else _DEFAULT_NAME}.py"


def _unique_name(name: str, taken: set[str]) -> str:
    """Add a numeric suffix to a file name until it is not taken."""
    stem = name.removesuffix(".py")
    candidate, number = name, 1
    while candidate in taken:
        number += 1
        candidate = f"{stem}_{number}.py"
    taken.add(candidate)
    return candidate


def build_memory(
    bugs: Sequence[Bug],
    store: ErrorStore,
    *,
    workdir: Path | None = None,
) -> list[MemoryEntry]:
    """Run every bug through the capture code and record its reference fix.

    Args:
        bugs: The bugs to record, in order (error ids follow that order in a new store).
        store: The store to fill; it should be empty so that every bug gets its own record.
        workdir: A folder to run the scripts in (a temporary one by default).

    Returns:
        One entry per bug, in the same order.

    Raises:
        MemoryBuildError: If a bug does not fail, or has the same fingerprint as an earlier bug
            (the ground truth would then be ambiguous).
    """
    if workdir is None:
        with tempfile.TemporaryDirectory() as temporary:
            return build_memory(bugs, store, workdir=Path(temporary))

    names: set[str] = set()
    owners: dict[int, str] = {}
    entries = []
    for bug in bugs:
        source = bug.buggy_path.read_text(encoding="utf-8")
        name = _unique_name(script_name_for(source), names)
        script = workdir / name
        script.write_text(source, encoding="utf-8")

        result = run_and_capture([sys.executable, str(script)], store, cwd=workdir)
        recorded = result.recorded
        if recorded is None:
            message = (
                f"{bug.id}: no error was recorded (exit code {result.exit_code}); "
                "buggy.py is supposed to fail"
            )
            raise MemoryBuildError(message)
        if recorded.error_id in owners:
            message = (
                f"{bug.id} has the same fingerprint as {owners[recorded.error_id]}; "
                "the evaluation could not tell them apart"
            )
            raise MemoryBuildError(message)

        owners[recorded.error_id] = bug.id
        store.add_fix(recorded.error_id, note=bug.fix_summary)
        entries.append(MemoryEntry(bug.id, recorded.error_id, recorded.fingerprint, name))
    return entries
