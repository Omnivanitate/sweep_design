from pathlib import Path
from typing import Union
from ...config import Config
from ...named_signals import NamedRelation


class ExtensionFileError(Exception):
    pass


def get_path_file_name(relation, file_name: Union[Path, str] = None, suffix="") -> Path:

    if file_name is None:
        if isinstance(relation, NamedRelation):
            file_name = f"{str(relation)}{suffix}"
        else:
            file_name = f"unnamed{suffix}"

    if isinstance(file_name, str):
        file_name = Path(file_name)

    if not file_name.is_absolute():
        file_name = Config.DEFAULT_PATH / file_name

    if file_name.suffix == "":
        file_name = file_name.parent / f"{file_name.name}{suffix}"

    if file_name.suffix != suffix:
        raise ExtensionFileError(
            f"The subbmited file_name {file_name} do not match extansion {suffix}"
        )

    return file_name
