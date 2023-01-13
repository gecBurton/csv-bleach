This command line tool sanitizes your CSV by:
1. detecting its encoding and converting it to utf-8
2. detecting its delimiter and safely converting it to a comma
3. casting all variables to json form, i.e. integers, floats, booleans, string or null.


A pypi build is not available yet so checkout the code, build it `poetry build`, and run like `poetry run bleach my-data.csv`

The only option is the output file name, by default it will be your original file name with `.scsv` extension.

You will now be able to parse your CSV safely with a simple script like:

```python
import json


def parse_row(text):
    return json.loads(f"[{text}]")


with open("my-data.scsv") as f:
    header = parse_row(next(f))
    for row in f:
        print(dict(zip(header, parse_row(row))))
```
