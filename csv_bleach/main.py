import logging
import os
from typing import Optional

import click

from csv_bleach.detect_encoding import detect_encoding
from csv_bleach.detect_rows_count import count_rows
from csv_bleach.type_casting import infer_types

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
        encoding = detect_encoding(input_file)  # type: ignore

    # with open(file, encoding=encoding) as input_file:  # type: ignore
    #     row_count = count_rows(input_file)  # type: ignore

    with open(file, encoding=encoding) as input_file:  # type: ignore
        type_caster = infer_types(input_file)  # type: ignore

    with open(file, encoding=encoding) as input_file, open(output, "w") as output_file:
        type_caster.process_file(input_file, output_file, row_count)


if __name__ == "__main__":
    cli()
