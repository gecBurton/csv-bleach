import pytest

from csv_bleach.line_decoder import parse_line


@pytest.mark.parametrize(
    "line, delimiter, expected_str, expected_count",
    [
        ("", ",", "", 0),
        (
            '"Joan ""the bone"", Anne",Jet,"9th, at Terrace plc",Desert City,CO,00123',
            ",",
            '"Joan \\"the bone\\", Anne", "Jet", "9th, at Terrace plc", "Desert City", "CO", "00123"',
            6,
        ),
        (
            '"Joan "the bone", Anne",Jet,"9th, at Terrace plc",Desert\\, City,CO,00123',
            ",",
            '"Joan \\"the bone\\", Anne", "Jet", "9th, at Terrace plc", "Desert\\\\, City", "CO", "00123"',
            6,
        ),
        (
            ",85+,,2018-03-07 00:00:00,,150,Nothing,1,0,1,0,,27223,1,,,,",
            ",",
            'null, "85+", null, "2018-03-07 00:00:00", null, 150, "Nothing", 1, "0", 1, "0", null, 27223, 1, null, null, null, null',
            18,
        ),
        (
            "17937�NAA01�Clinic�UNKNOWN�Visible�False�St Chads Clinic�St. Chads Drive���Liverpool�Merseyside�L32 8RE�53.482593536376953�-2.8844137191772461����",
            "�",
            '17937, "NAA01", "Clinic", "UNKNOWN", "Visible", false, "St Chads Clinic", "St. Chads Drive", null, null, "Liverpool", "Merseyside", "L32 8RE", 53.48259353637695, -2.884413719177246, null, null, null, null',
            19,
        ),
        (',"kevin"\n', ",", 'null, "kevin"', 2),
    ],
)
def test_split_line(line, delimiter, expected_str, expected_count):
    assert parse_line(line, delimiter) == (expected_str, expected_count)
