# my_module.pyx
from typing import List

SPECIAL = {b"true": b"true", b"false": b"false", b"null": b"null", b"": b"null", b"n/a": b"null"}

def json_encode_primitive(bytes txt) -> bytes:
    clean_text = txt.strip().replace(b'"', br'\"')
    if not clean_text:
        return b"null"

    try:
        return SPECIAL[clean_text.lower()]
    except KeyError:
        pass

    if clean_text[0] != b"0"[0]:
        try:
            float(clean_text)
            return clean_text
        except ValueError:
            pass

    return b'"' + clean_text + b'"'


def parse_line(text: bytes, delimiter: bytes, expected_count: int) -> bytes:
    text = text.rstrip(b"\n").replace(b'""', b'\\"')

    if not text:
        return b""

    fields: List[bytes] = [b"" for _ in range(expected_count)]
    current_field: bytes = b""
    is_quoted: bool = False
    is_escaped: bool = False
    i: int = 0

    for c in text:
        char = bytes([c])
        if char == delimiter and not is_quoted:
            if is_escaped:
                current_field += b"\\" + char
            else:
                fields[i] = json_encode_primitive(current_field)
                i += 1
                current_field = b""
        elif char == b'"':
            if is_escaped:
                current_field += char
            else:
                is_quoted = not is_quoted

        elif char == b"\\":
            is_escaped = not is_escaped
        else:
            is_escaped = False
            current_field += char

    fields[i] = json_encode_primitive(current_field)

    if expected_count != i + 1:
        raise ValueError(  # pragma: no cover
            f"expected {expected_count} got: {i+1}, original: `{text}`"
        )

    return b", ".join(fields)
