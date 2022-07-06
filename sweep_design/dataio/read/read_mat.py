from pathlib import Path
from typing import Union

from scipy.io import loadmat

from ...math_signals import Relation
from .defaults import get_read_file_name


def read_mat_file(file_name: Union[Path, str]) -> Relation:
    """Read data from mat file."""
    file_name = get_read_file_name(file_name)
    data = loadmat(file_name)
    print(data)
    columns = [column for column in data.values()]
    return Relation(x=columns[3][0], y=columns[4][0])
