import json
import logging
from typing import Any, Iterator, TextIO, List

import click

from csv_bleach.detect_delimiter import DelimiterDetector
from csv_bleach.line_decoder import LineSplit

LOG = logging.getLogger(__name__)
SPECIAL = {"true": True, "false": False, "null": None, "": None, "n/a": None}


def type_cast_element(txt: str):
    clean_text = txt.strip()
    if not clean_text:
        return None

    if clean_text[0] == '"' and clean_text[-1] == '"':
        clean_text = clean_text[1:-1]

    try:
        return SPECIAL[clean_text.lower()]
    except KeyError:
        pass

    if clean_text[0] != "0":
        try:
            return int(clean_text)
        except ValueError:
            pass

        try:
            return float(clean_text)
        except ValueError:
            pass

    return clean_text.replace('""', '"')


class TypeCaster:
    def __init__(self, delimiter: str, count: int):
        self.delimiter = LineSplit(delimiter)
        self.count = count
        assert self.count > 0

    def type_cast_row(self, i: int, txt: str) -> List[Any]:
        words = list(map(type_cast_element, self.delimiter.split_line(txt)))

        assert (
            len(words) == self.count
        ), f"line: {i}, expected {self.count} got: {len(words)}, original: `{txt}`, split: {words}"

        return words

    def parse_file(self, rows: TextIO) -> Iterator[list]:
        for i, row in enumerate(rows):
            if len(row.strip()) > 0:
                typed_row = self.type_cast_row(i, row)
                yield typed_row

    def process_file(self, input_file: TextIO, output_file: TextIO, row_count: int):
        with click.progressbar(
            self.parse_file(input_file),
            length=row_count,
            label="writing new file",
        ) as rows:
            for row in rows:
                json_row = json.dumps(row)[1:-1] + "\n"
                output_file.write(json_row)


def infer_types(rows: TextIO) -> TypeCaster:
    def _read(_rows):
        for row in _rows:
            if len(row.strip()) > 0:
                yield DelimiterDetector.parse_row(row)

    dd = DelimiterDetector.combine(_read(rows))
    assert len(dd.delimiter_count) == 1, dd.delimiter_count
    (_delimiter, _count), *_ = dd.delimiter_count.items()
    return TypeCaster(delimiter=_delimiter, count=_count + 1)
