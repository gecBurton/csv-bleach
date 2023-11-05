import pytest

from csv_bleach.infer_schema import Schema, get_schema_for_file


@pytest.mark.parametrize(
    "items, expected",
    [
        ([-4, 1, 4, 23], {"maximum": 23, "minimum": -4, "type": "integer"}),
        ([-0.4, 0.1, 4.23], {"maximum": 4.23, "minimum": -0.4, "type": "number"}),
        ([False, True], {"type": "boolean"}),
        ([None], {"type": "null"}),
        (["cat", "dog", "fish"], {"maxLength": 4, "minLength": 3, "type": "string"}),
        (
            [-4, None, 1, 4, 23],
            {"maximum": 23, "minimum": -4, "type": ["integer", "null"]},
        ),
        (
            [-0.4, 0.1, None, 4.23],
            {"maximum": 4.23, "minimum": -0.4, "type": ["number", "null"]},
        ),
        ([False, True, None], {"type": ["boolean", "null"]}),
        (
            ["cat", "dog", "fish", None],
            {"maxLength": 4, "minLength": 3, "type": ["string", "null"]},
        ),
        (
            [-4.0, None, 1, 4, 23],
            {
                "oneOf": [
                    {"maximum": -4.0, "minimum": -4.0, "type": "number"},
                    {"maximum": 23, "minimum": 1, "type": "integer"},
                ]
            },
        ),
    ],
)
def test_schema(items, expected):
    schema = Schema()
    for item in items:
        schema.add(item)
    assert schema.to_dict() == expected


def test_get_schema_for_file():
    with open("tests/real-world-data/cleaned/complex.csv") as f:
        schema = get_schema_for_file(f)

    expected_age = {"maxLength": 6, "minLength": 5, "type": ["string", "null"]}
    expected_name_int = {"maximum": 12, "minimum": 12, "type": "integer"}
    expected_name_str = {"maxLength": 6, "minLength": 6, "type": "string"}
    expected_name_float = {"maximum": 13.5, "minimum": 13.5, "type": "number"}

    actual = {k: v.to_dict() for k, v in schema.items()}
    assert actual["age"] == expected_age
    assert expected_name_int in actual["name"]["oneOf"]
    assert expected_name_str in actual["name"]["oneOf"]
    assert expected_name_float in actual["name"]["oneOf"]
