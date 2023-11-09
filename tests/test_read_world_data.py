import os

import pytest
from click.testing import CliRunner

from csv_bleach.main import cli

dir_path = os.path.dirname(os.path.realpath(__file__))
INPUT_FILES = os.listdir(os.path.join(dir_path, "real-world-data", "examples"))


@pytest.mark.parametrize("file", INPUT_FILES)
def test_real_world_data(file):
    example_file_path = os.path.join(dir_path, "real-world-data", "examples", file)
    cleaned_file_path = os.path.join(dir_path, "real-world-data", "cleaned", file)

    runner = CliRunner()

    with open(cleaned_file_path) as f:
        expected = f.read()

    with runner.isolated_filesystem():
        result = runner.invoke(cli, [example_file_path, "--output", "out.csv"])
        assert result.exit_code == 0

        with open("out.csv") as f:
            assert f.read() == expected
