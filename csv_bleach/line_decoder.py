import json
from typing import List, Tuple

__all__ = ["parse_line"]

SPECIAL = {"true": True, "false": False, "null": None, "": None, "n/a": None}


def type_cast_element(txt: str):
    clean_text = txt.strip()
    if not clean_text:
        return None

    if clean_text[0] == '"' and clean_text[-1] == '"':
        clean_text = clean_text[1:-1]

    try:
        return SPECIAL[clean_text.lower()]
    except KeyError:
        pass

    if clean_text[0] != "0":
        try:
            return int(clean_text)
        except ValueError:
            pass

        try:
            return float(clean_text)
        except ValueError:
            pass

    return clean_text.replace('""', '"')


def split_text(text: str, delimiter: str) -> List[str]:
    if not text:
        return []

    fields = []
    current_field = ""
    in_quotes = False
    escape = False

    for char in text.rstrip("\n").replace('""', '"'):
        if char == delimiter and not in_quotes:
            if not escape:
                fields.append(current_field)
                current_field = ""
            else:
                current_field += "\\" + char
        elif char == '"':
            if not escape:
                in_quotes = not in_quotes
            else:
                current_field += "\\"  # pragma: no cover
            current_field += char
        elif char == "\\":
            escape = not escape
        else:
            escape = False
            current_field += char

    fields.append(current_field)
    return fields


def parse_line(text: str, delimiter: str) -> Tuple[str, int]:
    fields = list(map(type_cast_element, split_text(text, delimiter)))
    return json.dumps(fields)[1:-1], len(fields)
