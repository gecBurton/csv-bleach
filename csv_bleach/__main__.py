import logging
import os
from typing import Optional

import click

from csv_bleach.detect_row_count import detect_row_count
from csv_bleach.line_decoder import LineSplit
from csv_bleach.type_casting import infer_types, process_file

logging.basicConfig(level=logging.INFO)


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
        row_count = detect_row_count(input_file)

    with open(file, "rb") as input_file:
        delimiter, column_count = infer_types(input_file)

    with open(file, "rb") as input_file, open(output, "w") as output_file:
        process_file(
            LineSplit(delimiter), column_count, input_file, output_file, row_count
        )


if __name__ == "__main__":
    cli()  # pragma: no cover
