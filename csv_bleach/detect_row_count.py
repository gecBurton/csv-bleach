from typing import BinaryIO


def blocks(files, size=65536):
    while True:
        b = files.read(size)
        if not b:
            break
        yield b


def detect_row_count(file: BinaryIO) -> int:
    return sum(bl.count("\n") for bl in blocks(file))