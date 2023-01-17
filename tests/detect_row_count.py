from io import BytesIO

import pytest

from csv_bleach.detect_row_count import detect_row_count


@pytest.mark.xfail
@pytest.mark.parametrize(
    "text, count", [("", 0), ("hello", 0), ("hello\n", 1), ("hello\nto\nyou", 2)]
)
def test_detect_row_count(text, count):
    file = BytesIO(text.encode())
    assert detect_row_count(file) == count
