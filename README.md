# clean your CSVs!

This command line tool cleans CSV files by:
1. detecting the encoding and converting it to utf-8
2. detecting the delimiter and safely converting it to a comma
3. casting all variables to json form, i.e. integers, floats, booleans, string or null.


* install `pip install csv-bleach`
* and run like `python -m run csv_bleach my-data.csv`

The only option is the output file name, by default it will be your original file name with `.scsv` extension.

You will now be able to parse your CSV safely with a simple script like:

```python
import json


def parse_row(text):
    return json.loads(f"[{text}]")

def parse_file(file):
    rows = map(parse_row, file)
    header = next(rows)
    for row in rows:
        yield dict(zip(header, row))


with open("my-data.scsv") as f:
    for item in parse_file(f):
        print(item)
```
