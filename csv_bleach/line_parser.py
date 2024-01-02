from charset_normalizer import from_bytes


def binary_to_utf8(raw: bytes) -> str:
    """converty bytes to utf8 str"""
    try:
        return raw.decode()
    except UnicodeError:
        return str(from_bytes(raw).best())
