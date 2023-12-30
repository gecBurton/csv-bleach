import pytest

from csv_bleach.detect_delimiter import DelimiterDetector, combine


@pytest.mark.parametrize(
    "txt, result",
    [
        (
            b'a,b|c,e;;f g,"i"|, k',
            DelimiterDetector({" ": 2, ",": 4, ";": 2, "|": 2}),
        ),
        (b"a b c   d", DelimiterDetector({" ": 3})),
        (
            b'"Joan ""the bone"", Anne",Jet,"9th, at Terrace plc",Desert City,CO,00123',
            DelimiterDetector({",": 5, " ": 1}),
        ),
        (
            b"a   b   c",
            DelimiterDetector({" ": 2}),
        ),
    ],
)
def test_parse(txt, result):
    assert DelimiterDetector.parse_row(txt) == result


def test_parse_fails():
    with pytest.raises(ValueError) as type_error:
        DelimiterDetector.parse_row(b'a, "b, c')
    assert type_error.value.args == ('row not escaped: `a, "b, c`',)


def test_combine_1():
    items = [
        DelimiterDetector({",": 3, ";": 2, "|": 1}),
        DelimiterDetector({",": 3, ";": 2, "|": 12}),
        DelimiterDetector({",": 3, "|": 1}),
    ]
    assert combine(iter(items)) == DelimiterDetector({",": 3})


def test_combine_2():
    items = [
        DelimiterDetector({",": 3, " ": 2}),
        DelimiterDetector({",": 3, " ": 2}),
    ]
    assert combine(iter(items)) == DelimiterDetector({",": 3})


def test_combine_fail():
    items = [
        DelimiterDetector({",": 3}),
        DelimiterDetector({"|": 3}),
    ]
    with pytest.raises(ValueError) as value_error:
        combine(iter(items))
    assert value_error.value.args == ("no delimiter detected in file",)
