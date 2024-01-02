from __future__ import annotations

import collections
from typing import Iterator

from csv_bleach.line_parser import binary_to_utf8

QUOTE = 34
NEW_LINE = 10
CARRIAGE_RETURN = 13


class DelimiterDetector:
    def __init__(self, delimiter_count: dict[str, int]):
        self.delimiter_count = delimiter_count

    @classmethod
    def parse_row(cls, raw: bytes) -> DelimiterDetector:
        txt = binary_to_utf8(raw)
        escaped = False
        chars = []
        prev = None
        for char in txt:
            if ord(char) == QUOTE:
                escaped = not escaped

            if (
                not escaped
                and not char.isalnum()
                and not (char.isspace() and prev and prev.isspace())
                and ord(char) not in (NEW_LINE, QUOTE, CARRIAGE_RETURN)
            ):
                chars.append(char)

            prev = char

        if escaped:
            raise ValueError(f"row not escaped: `{txt}`")
        special_chars = collections.Counter(chars)
        return cls(dict(special_chars))

    def __eq__(self, other):
        return self.delimiter_count == other.delimiter_count


def combine(rows: Iterator[DelimiterDetector]) -> DelimiterDetector:
    current = next(rows)
    for row in rows:
        intersection = {
            key: value
            for key, value in current.delimiter_count.items()
            if key in row.delimiter_count
            and current.delimiter_count[key] == row.delimiter_count[key]
        }
        current = DelimiterDetector(intersection)
        if len(current.delimiter_count) == 1:
            return current
        if len(current.delimiter_count) == 2:
            if " " in current.delimiter_count:
                current.delimiter_count.pop(" ")
                return current
    raise ValueError("no delimiter detected in file")
