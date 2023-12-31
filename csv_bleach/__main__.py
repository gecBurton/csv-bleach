import logging
import os
from typing import Optional

import click
from charset_normalizer import from_bytes

from csv_bleach.detect_delimiter import infer_delimiter
from csv_bleach.json_encode import parse_line

logging.basicConfig(level=logging.INFO)

__all__ = ["cli"]


@click.command()
@click.argument("file", type=click.Path(exists=True))
@click.option(
    "--output", type=click.Path(exists=False), help="output file", default=None
)
def cli(file: str, output: Optional[str]):
    """file: input csv file"""
    logging.basicConfig(level=logging.INFO)
    if output is None:
        filepath, _ = os.path.splitext(file)
        output = f"{filepath}.scsv"

    with open(file, "rb") as input_file:
        row_count = sum(1 for _ in iter(input_file))

    with open(file, "rb") as input_file:
        delimiter, column_count = infer_delimiter(input_file)

    with open(file, "rb") as input_file, open(output, "wb") as output_file:
        with click.progressbar(input_file, length=row_count) as rows:
            for i, row in enumerate(rows):
                try:
                    utf8_str = row.decode()
                except UnicodeError:
                    utf8_str = str(from_bytes(row).best())
                json_str = parse_line(utf8_str, delimiter, column_count)
                output_file.write(json_str + "\n")


if __name__ == "__main__":
    cli()  # pragma: no cover
