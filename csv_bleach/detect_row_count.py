from typing import BinaryIO


def detect_row_count(file: BinaryIO) -> int:
    return sum(1 for _ in file)
