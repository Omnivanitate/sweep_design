from enum import Enum
from pathlib import Path
from typing import Literal, Tuple, Union

from ...math_signals import Relation
from ...named_signals import NamedRelation
from .write_mat import write_mat_file
from .write_txt import write_txt_file


class FileType(Enum):
    MAT = ".mat"
    TXT = ".txt"


def write_data(
    relation: Union[Relation, NamedRelation],
    file_name: Union[Path, str] = None,
    header: Tuple[str, str] = None,
    file_type: Literal[".mat", ".txt"] = None,
) -> None:

    """This is a common function to write data."""

    if isinstance(file_name, str):
        file_name = Path(file_name)

    suffix = file_name.suffix

    if suffix == FileType.MAT.value or file_type == FileType.MAT.value:
        write_mat_file(relation, file_name, header)
    else:
        write_txt_file(relation, file_name, header)
