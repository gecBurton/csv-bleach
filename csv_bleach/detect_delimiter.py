from __future__ import annotations

import collections
import logging
from typing import Iterator

QUOTE = 34
NEW_LINE = 10


class DelimiterDetector:
    def __init__(self, delimiter_count: dict[str, int]):
        self.delimiter_count = delimiter_count

    @classmethod
    def parse_row(cls, txt: str) -> DelimiterDetector:
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
                and ord(char) not in (NEW_LINE, QUOTE)
            ):
                chars.append(char)

            prev = char

        if escaped:
            raise ValueError(f"row not escaped: `{txt}`")
        special_chars = collections.Counter(chars)
        return cls(dict(special_chars))

    def __eq__(self, other):
        return self.delimiter_count == other.delimiter_count

    @classmethod
    def combine(cls, rows: Iterator[DelimiterDetector]) -> DelimiterDetector:
        def _combine(
            left: DelimiterDetector, right: DelimiterDetector
        ) -> DelimiterDetector:
            intersection = {
                key: value
                for key, value in left.delimiter_count.items()
                if key in right.delimiter_count
                and left.delimiter_count[key] == right.delimiter_count[key]
            }
            return cls(intersection)

        def log(row_number):
            k, *_ = list(current.delimiter_count.keys())
            logging.info(
                f"`{k}` has been identified as the delimiter after {row_number+1} rows"
            )

        current = next(rows)
        for i, row in enumerate(rows):
            current = _combine(current, row)
            if len(current.delimiter_count) == 1:
                log(i)
                return current
            if len(current.delimiter_count) == 2:
                if " " in current.delimiter_count:
                    current.delimiter_count.pop(" ")
                    log(i)
                    return current
        raise ValueError("no delimiter detected in file")
