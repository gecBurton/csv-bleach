from typing import IO


def blocks(files, size=65536):
    while True:
        b = files.read(size)
        if not b:
            break
        yield b


def detect_row_count(file: IO[str]) -> int:
    return sum(bl.count("\n") for bl in blocks(file))
