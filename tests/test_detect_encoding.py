from io import BytesIO

import pytest

from csv_bleach.detect_encoding import detect_encoding


@pytest.mark.parametrize(
    "text, encoding",
    [
        ("abc, 123", "ascii"),
        ("Σὲ γνωρίζω ἀπὸ τὴν κόψη", "utf-8"),
    ],
)
def test_detect_encoding(text, encoding):
    file = BytesIO(text.encode(encoding=encoding))
    assert detect_encoding(file) == encoding
