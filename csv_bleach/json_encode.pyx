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
