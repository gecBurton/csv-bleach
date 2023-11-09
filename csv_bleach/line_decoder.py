from typing import List


def custom_parser(text: str, delimiter: str) -> List[str]:
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
                current_field += "\\"
            current_field += char
        elif char == "\\":
            escape = not escape
        else:
            escape = False
            current_field += char

    fields.append(current_field)
    return fields
