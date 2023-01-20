import pytest

from bleach.type_casting import TypeCaster, type_cast_element


@pytest.mark.parametrize(
    "txt, expected",
    [
        (
            '"John ""Da Man""",Repici,120 Jefferson St.,Riverside, NJ,08075',
            [
                'John "Da Man"',
                "Repici",
                "120 Jefferson St.",
                "Riverside",
                "NJ",
                "08075",
            ],
        ),
        (
            '"Joan ""the bone"", Anne",Jet,"9th, at Terrace plc",Desert City,CO,00123',
            [
                'Joan "the bone", Anne',
                "Jet",
                "9th, at Terrace plc",
                "Desert City",
                "CO",
                "00123",
            ],
        ),
    ],
)
def test_type_cast_row(txt, expected):
    tc = TypeCaster(delimiter=",", count=6)
    actual = tc.type_cast_row(0, txt)
    assert actual == expected


@pytest.mark.parametrize(
    "element, expected",
    [
        ("", None),
        ("True", True),
        ("FALSE", False),
        ("null", None),
        ("1.45", 1.45),
        ("01.45", "01.45"),
    ],
)
def test_type_cast_element(element, expected):
    assert type_cast_element(element) == expected
