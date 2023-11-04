import pytest

from csv_bleach.line_decoder import LineSplit


@pytest.mark.parametrize(
    "line, delimiter, result",
    [
        ("", ",", []),
        (
            r'"Joan ""the bone"", Anne",Jet,"9th, at Terrace plc",Desert City,CO,00123\n',
            ",",
            [
                '"Joan ""the bone"", Anne"',
                "Jet",
                '"9th, at Terrace plc"',
                "Desert City",
                "CO",
                "00123\\n",
            ],
        ),
        (
            r'"Joan \"the bone\", Anne",Jet,"9th, at Terrace plc",Desert\, City,CO,00123\n',
            ",",
            [
                '"Joan \\"the bone\\", Anne"',
                "Jet",
                '"9th, at Terrace plc"',
                "Desert\\",
                " City",
                "CO",
                "00123\\n",
            ],
        ),
        (
            r",85+,,2018-03-07 00:00:00,,150,Nothing,1,0,1,0,,27223,1,,,,\n",
            ",",
            [
                "",
                "85+",
                "",
                "2018-03-07 00:00:00",
                "",
                "150",
                "Nothing",
                "1",
                "0",
                "1",
                "0",
                "",
                "27223",
                "1",
                "",
                "",
                "",
                "\\n",
            ],
        ),
        (
            r"17937�NAA01�Clinic�UNKNOWN�Visible�False�St Chads Clinic�St. Chads Drive���Liverpool�Merseyside�L32 8RE�53.482593536376953�-2.8844137191772461����",
            "�",
            [
                "17937",
                "NAA01",
                "Clinic",
                "UNKNOWN",
                "Visible",
                "False",
                "St Chads Clinic",
                "St. Chads Drive",
                "",
                "",
                "Liverpool",
                "Merseyside",
                "L32 8RE",
                "53.482593536376953",
                "-2.8844137191772461",
                "",
                "",
                "",
                "",
            ],
        ),
        (',"kevin"\n', ",", ["", '"kevin"']),
    ],
)
def test_split_line(line, delimiter, result):
    ls = LineSplit(delimiter)
    assert ls.split_line(line) == result
