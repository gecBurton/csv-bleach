from io import StringIO

import pytest

from csv_bleach.detect_row_count import detect_row_count


@pytest.mark.parametrize(
    "text, count", [("", 0), ("hello", 1), ("hello\n", 1), ("hello\nto\nyou", 3)]
)
def test_detect_row_count(text, count):
    file = StringIO(text)
    assert detect_row_count(file) == count
