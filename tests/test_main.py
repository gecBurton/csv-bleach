from click.testing import CliRunner

from csv_bleach.main import cli

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

        def parse_row(text: str) -> list:
            return json.loads(f"[{text}]")

        with open("THE_SIMPSONS.scsv") as f:
            header, *rows = map(parse_row, f)
            assert header == ["name", "age"]
            assert rows == [["bart", 10], ["lisa", 8], ["maggie", 1]]
