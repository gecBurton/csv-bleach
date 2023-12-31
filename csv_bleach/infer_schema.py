import json
from collections import defaultdict
from typing import Any, Optional, Type


def get_bound(value):
    if value is None:
        return 0
    if isinstance(value, bool):
        return 0
    return len(value) if isinstance(value, str) else value


class Schema:
    def __init__(self):
        self.type = set()
        self.min = {}
        self.max = {}
        self.count = defaultdict(int)

    def add(self, value):
        t = type(value)
        self.type = self.type | {t}

        m = get_bound(value)
        self.min[t] = min(self.min[t], m) if t in self.min else m
        self.max[t] = max(self.max[t], m) if t in self.max else m

        if self.count is not None:
            self.count[value] += 1

    #            if len(self.count) > 10:
    #                if len(self.count) / sum(self.count.values())

    def single(self, t: Optional[Type]):
        if t == int:
            return {"type": "integer", "minimum": self.min[t], "maximum": self.max[t]}
        if t == float:
            return {"type": "number", "minimum": self.min[t], "maximum": self.max[t]}
        if t == bool:
            return {"type": "boolean"}
        if t == str:
            return {
                "type": "string",
                "minLength": self.min[t],
                "maxLength": self.max[t],
            }
        return None

    def to_dict(self):
        types = []
        null = False
        for _type in self.type:
            if t := self.single(_type):
                types.append(t)
            else:
                null = True

        if len(types) == 0 and null:
            return {"type": "null"}

        if len(types) == 1 and not null:
            return types[0]

        if len(types) == 1 and null:
            types[0]["type"] = [types[0]["type"], "null"]
            return types[0]

        return {"oneOf": types}


def parse_row(txt):
    return json.loads(f"[{txt}]")


def get_schema_for_file(f) -> dict[str, Schema]:
    header = parse_row(next(f))
    schema = {col: Schema() for col in header}
    for row in f:
        for field, value in zip(header, parse_row(row)):
            schema[field].add(value)
    return schema
