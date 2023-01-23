from click.testing import CliRunner

from csv_bleach.__main__ import cli

THE_SIMPSONS = "name,age\nbart,10\nlisa,8\nmaggie,1"


def test_cli():
    """end-to-end test using the code from the README to check that everything works"""
    runner = CliRunner()

    with runner.isolated_filesystem():

        with open("THE_SIMPSONS.csv", "w", encoding="latin") as f:
            f.write(THE_SIMPSONS)

        result = runner.invoke(cli, ["THE_SIMPSONS.csv"])
        assert result.exit_code == 0

        import json
        from typing import IO, Iterable

        def parse_row(text: str) -> list:
            return json.loads(f"[{text}]")

        def parse_file(file: IO[str]) -> Iterable[dict]:
            rows = map(parse_row, file)
            header = next(rows)
            for row in rows:
                yield dict(zip(header, row))

        with open("THE_SIMPSONS.scsv") as f:
            expected = [
                {"age": 10, "name": "bart"},
                {"age": 8, "name": "lisa"},
                {"age": 1, "name": "maggie"},
            ]
            assert list(parse_file(f)) == expected
