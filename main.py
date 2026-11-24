#!/usr/bin/env python3
"""Entry for 'Fortune Cookie Wisdom for Developers'.

Writes one original fortune-cookie line for a software developer to
/output/entry.txt, then verifies the written file round-trips exactly.
Standard library only; no network access.
"""

import os
import sys

LINE = (
    "The legacy code you curse was written by someone in a hurry, "
    "just like you are now."
)

OUTPUT_PATH = "/output/entry.txt"


def main() -> int:
    if not LINE or not LINE.strip():
        print("error: entry is empty or only whitespace", file=sys.stderr)
        return 1
    if "\n" in LINE or "\r" in LINE:
        print("error: entry must be a single line", file=sys.stderr)
        return 1
    if not 1 <= len(LINE) <= 120:
        print(
            f"error: entry is {len(LINE)} characters, must be 1-120",
            file=sys.stderr,
        )
        return 1
    # The gate reads the file as UTF-8, so confirm the bytes decode back
    # to exactly the same text before we ever write it.
    if LINE.encode("utf-8").decode("utf-8") != LINE:
        print("error: entry does not round-trip through UTF-8", file=sys.stderr)
        return 1

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8", newline="\n") as f:
        f.write(LINE + "\n")

    raw = open(OUTPUT_PATH, "rb").read()
    if raw.decode("utf-8") != LINE + "\n":
        print("error: written file does not round-trip exactly", file=sys.stderr)
        return 1

    print(f"wrote {len(LINE)} characters to {OUTPUT_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
