# clean your CSVs!

This command line tool rationalizes CSV files by:
1. detecting the encoding and converting it to utf-8
2. detecting the delimiter and safely converting it to a comma
3. casting all variables to json form, i.e. integers, floats, booleans, string or null.


A pypi build is not available yet so checkout the code, build it `poetry build`, and run like `poetry run bleach my-data.csv`

The only option is the output file name, by default it will be your original file name with `.scsv` extension.

You will now be able to parse your CSV safely with a simple script like:

```python
import json


def parse_row(text: str) -> list:
    return json.loads(f"[{text}]")


with open("my-data.scsv") as f:
    header, *rows = map(parse_row, f)
    for row in rows:
        print(dict(zip(header, row)))
```
