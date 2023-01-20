"""https://gist.github.com/awwsmm/886ac0ce0cef517ad7092915f708175f
"""
import re
from typing import List


class LineSplit:
    def __init__(self, delimiter: str):
        self.regex = re.compile(
            f'(?:{delimiter}|\\n|^)("(?:(?:"")*(?:[^"\\\\]|\\\\.)*[^"]*)*"|[^"{delimiter}\\n]*|(?:\\n|$))'
        )

    def split_line(self, txt: str) -> List[str]:
        if not txt:
            return []
        if (
            txt[0] == ","
        ):  # nasty hack to force the regex to detect an empty initial variable
            txt = "," + txt
        split = re.findall(self.regex, txt.rstrip("\n"))
        return split
