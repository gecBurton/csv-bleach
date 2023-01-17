from io import BytesIO

import pytest

from csv_bleach.detect_encoding import detect_encoding


@pytest.mark.parametrize(
    "text, encoding", [("abc, 123", "ASCII"), ("Σὲ γνωρίζω ἀπὸ τὴν κόψη", "UTF-8")]
)
def test_detect_encoding(text, encoding):
    file = BytesIO(text.encode())
    assert detect_encoding(file) == encoding
