import logging
import os
from typing import Optional

import click
from charset_normalizer import from_bytes

from csv_bleach.detect_delimiter import infer_delimiter
from csv_bleach.line_decoder import parse_line

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
        row_count = sum(1 for _ in input_file)

    with open(file, "rb") as input_file:
        delimiter, column_count = infer_delimiter(input_file)

    with open(file, "rb") as input_file, open(output, "w") as output_file:
        with click.progressbar(input_file, length=row_count) as rows:
            for i, row in enumerate(rows):
                utf8_str = str(from_bytes(row).best())
                json_str, actual_count = parse_line(utf8_str, delimiter)

                if actual_count != column_count:
                    raise ValueError(  # pragma: no cover
                        f"line: {i}, expected {column_count} got: {actual_count}, original: `{row.decode()}`"
                    )

                output_file.write(json_str + "\n")


if __name__ == "__main__":
    cli()  # pragma: no cover
