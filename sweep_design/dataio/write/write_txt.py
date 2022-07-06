from typing import Sequence, Union
from pathlib import Path

from loguru import logger

from ...math_signals import Relation
from ...named_signals import NamedRelation

from .default import get_path_file_name


def write_txt_file(
    relation: Union[Relation, NamedRelation],
    file_name: Union[str, Path] = None,
    header: Union[bool, Sequence[str]] = None,
) -> None:
    """Save the data to txt file."""
    file_name = get_path_file_name(
        relation, file_name, ".txt" if file_name is None else Path(file_name).suffix
    )

    x, y = relation.get_data()

    with file_name.open("w") as f:
        if header is None or header is True:
            f.write("x\ty\n")
        elif len(header) > 1:
            f.write(f"{header[0]}\t{header[1]}\n")

        f.writelines((f"{x}\t{y}\n" for x, y in zip(x, y)))

    logger.info("The file is saved in the following path: {}", file_name)
