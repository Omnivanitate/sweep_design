from pathlib import Path
from typing import Union

from .defaults import get_read_file_name

from ...math_signals import Relation


def read_txt_file(file_name: Union[Path, str], sep="\t") -> Relation:
    """Read data from txt file."""
    file_name = get_read_file_name(file_name)
    with file_name.open() as f:
        lines = [line.strip().split(sep) for line in f.readlines()]
        x = []
        y = []
        for line in lines:
            if len(line) > 1:
                if line[0].isalnum() and line[1].isalnum():
                    x.append(line[0])
                    y.append(line[1])

    return Relation(x, y)
