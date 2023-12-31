import pytest

from csv_bleach.json_encode import parse_line


@pytest.mark.parametrize(
    "line, delimiter, expected_str, expected_count",
    [
        (b"", b",", b"", 0),
        (
            b'"Joan ""the bone"", Anne",Jet,"9th, at Terrace plc",Desert City,CO,00123',
            b",",
            b'"Joan \\"the bone\\", Anne", "Jet", "9th, at Terrace plc", "Desert City", "CO", "00123"',
            6,
        ),
        (
            b'"Joan \\"the bone\\", Anne",Jet,"9th, at Terrace plc",Desert\\, City,CO,00123',
            b",",
            b'"Joan \\"the bone\\", Anne", "Jet", "9th, at Terrace plc", "Desert\\, City", "CO", "00123"',
            6,
        ),
        (
            b",85+,,2018-03-07 00:00:00,,150,Nothing,1,0,1,0,,27223,1,,,,",
            b",",
            b'null, "85+", null, "2018-03-07 00:00:00", null, 150, "Nothing", 1, "0", 1, "0", null, 27223, 1, null, null, null, null',
            18,
        ),
        (b',"kevin"\n', b",", b'null, "kevin"', 2),
    ],
)
def test_split_line(line, delimiter, expected_str, expected_count):
    assert parse_line(line, delimiter, expected_count) == expected_str
