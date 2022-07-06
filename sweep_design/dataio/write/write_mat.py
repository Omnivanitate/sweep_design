from pathlib import Path
from typing import Sequence, Union
from loguru import logger

from scipy.io import savemat

from ...math_signals import Relation
from ...named_signals import NamedRelation

from .default import get_path_file_name


def write_mat_file(
    relation: Union[Relation, NamedRelation],
    file_name: Union[Path, str] = None,
    header: Sequence[str] = None,
) -> None:
    """Save the data to mat file."""

    file_name = get_path_file_name(relation, file_name, suffix=".mat")

    x, y = relation.get_data()
    if header is None:
        header = "x", "y"

    data = {header[0]: x, header[1]: y}
    savemat(file_name, data)

    logger.info("The file is saved in the following path: {}", file_name)
