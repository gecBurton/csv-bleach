This command line tool sanitizes your CSV by:
1. detecting its encoding and converting it to utf-8
2. detecting its delimeter and safely converting it to a comma
3. casting all variables to json form, i.e. integers, floats, booleans, string or null.

No pypi build available yet so check the code, build it `poetry build`, and run `poetry run bleach my-csv`

You will now be be able to parse your CSV safely with a simple script like:

```python
with open("my-data.csv") as f:
    header = json.loads(next(f))
    for row in f:
        print(dict(zip(header, json.loads(f"[{row}]"))))
```
