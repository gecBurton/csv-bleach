from typing import List
from .json_encode import json_encode_primitive

SPECIAL = {"true": "true", "false": "false", "null": "null", "": "null", "n/a": "null"}

__all__ = ["parse_line"]


# def json_encode_primitive(txt: str) -> str:
#     clean_text = txt.strip().replace('"', r"\"")
#     if not clean_text:
#         return "null"
#
#     try:
#         return SPECIAL[clean_text.lower()]
#     except KeyError:
#         pass
#
#     if clean_text[0] != "0":
#         try:
#             float(clean_text)
#             return clean_text
#         except ValueError:
#             pass
#
#     return f'"{clean_text}"'


def parse_line(text: bytes, delimiter: bytes, expected_count: int) -> bytes:
    text = text.decode().rstrip("\n").replace('""', '\\"')

    if not text:
        return b""

    fields: List[str] = ["" for _ in range(expected_count)]
    current_field: str = ""
    is_quoted: bool = False
    is_escaped: bool = False
    i: int = 0

    for char in text:
        if char == delimiter and not is_quoted:
            if is_escaped:
                current_field += "\\" + char
            else:
                fields[i] = json_encode_primitive(current_field.encode()).decode()
                i += 1
                current_field = ""
        elif char == '"':
            if is_escaped:
                current_field += char
            else:
                is_quoted = not is_quoted

        elif char == "\\":
            is_escaped = not is_escaped
        else:
            is_escaped = False
            current_field += char

    fields[i] = json_encode_primitive(current_field.encode()).decode()

    if expected_count != i + 1:
        raise ValueError(  # pragma: no cover
            f"expected {expected_count} got: {i+1}, original: `{text}`"
        )

    return ", ".join(fields).encode()
