import json
import logging
from typing import Any, List, BinaryIO, TextIO

import click

from charset_normalizer import from_bytes
from csv_bleach.detect_delimiter import DelimiterDetector, combine
from csv_bleach.line_decoder import LineSplit

LOG = logging.getLogger(__name__)
SPECIAL = {"true": True, "false": False, "null": None, "": None, "n/a": None}


def binary_to_str(raw: bytes) -> str:
    try:
        return raw.decode()
    except UnicodeError:
        return str(from_bytes(raw).best())


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


def type_cast_row(
    delimiter: LineSplit, column_count: int, i: int, txt: str
) -> List[Any]:
    words = list(map(type_cast_element, delimiter.split_line(txt)))

    assert (
        len(words) == column_count
    ), f"line: {i}, expected {column_count} got: {len(words)}, original: `{txt}`, split: {words}"

    return words


def process_file(
    delimiter: LineSplit,
    column_count: int,
    input_file: BinaryIO,
    output_file: TextIO,
    row_count: int,
):
    with click.progressbar(length=row_count, label="writing new file") as bar:  # type: ignore
        for i, row in enumerate(input_file):
            str_row = binary_to_str(row)
            typed_row = type_cast_row(delimiter, column_count, i, str_row)
            json_row = json.dumps(typed_row)[1:-1] + "\n"
            output_file.write(json_row)
            bar.update(1)


def infer_types(rows: BinaryIO) -> tuple[str, int]:
    def _read(_rows):
        for row in _rows:
            str_row = binary_to_str(row)
            if len(str_row.strip()) > 0:
                yield DelimiterDetector.parse_row(str_row)

    dd = combine(_read(iter(rows)))
    assert len(dd.delimiter_count) == 1, dd.delimiter_count
    (_delimiter, _count), *_ = dd.delimiter_count.items()
    return _delimiter, _count + 1
