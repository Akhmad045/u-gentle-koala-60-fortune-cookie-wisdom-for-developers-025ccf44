#!/usr/bin/env python3
"""Fortune Cookie Wisdom for Developers — a make.fun entry.

This program holds one original fortune-cookie line written for a
software developer and places it in /output/entry.txt, the file the
competition gate reads. Before writing anything it checks the line
against the gate's rules: UTF-8 text, 1 to 120 characters, a single
line, nothing blank and no control characters. After writing it reads
the file back and confirms the bytes on disk are exactly the line it
meant to write.

Only the Python standard library is used, and nothing here touches
the network.
"""

import sys
from pathlib import Path

FORTUNE = (
    "The legacy code you curse was written by someone in a hurry, "
    "just like you are now."
)
DESTINATION = Path("/output/entry.txt")
LIMIT = 120


def problems(line):
    """List every way `line` breaks the gate rules (empty means fine)."""
    found = []
    if not line.strip():
        found.append("the line is empty or only whitespace")
    if line != line.strip():
        found.append("the line starts or ends with whitespace")
    if any(ch in line for ch in ("\n", "\r")):
        found.append("the line spans more than one line")
    if any(ord(ch) < 32 or ord(ch) == 127 for ch in line):
        found.append("the line holds a control character")
    if len(line) > LIMIT:
        found.append(
            f"the line is {len(line)} characters, over the {LIMIT} limit"
        )
    try:
        round_tripped = line.encode("utf-8").decode("utf-8")
    except UnicodeError:
        found.append("the line is not valid UTF-8 text")
    else:
        if round_tripped != line:
            found.append("the line does not survive a UTF-8 round trip")
    return found


def run():
    faults = problems(FORTUNE)
    if faults:
        for fault in faults:
            print(f"invalid entry: {fault}", file=sys.stderr)
        return 1

    DESTINATION.parent.mkdir(parents=True, exist_ok=True)
    with DESTINATION.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(FORTUNE + "\n")

    on_disk = DESTINATION.read_bytes()
    wanted = (FORTUNE + "\n").encode("utf-8")
    if on_disk != wanted:
        print(
            "invalid entry: the file on disk differs from the line",
            file=sys.stderr,
        )
        return 1

    print(f"entry written: {len(FORTUNE)} characters in {DESTINATION}")
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
