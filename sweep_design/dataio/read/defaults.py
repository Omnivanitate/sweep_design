from pathlib import Path
from typing import Union

from ...config import Config


class FileNotFoundError(Exception):
    """Raise an exception if the file is not found."""

    pass


def get_read_file_name(file_name: Union[Path, str]):
    """Define the file name to be read."""
    if isinstance(file_name, str):
        file_name = Path(file_name)

    if not file_name.is_absolute():
        file_name = Config.DEFAULT_PATH / file_name

    if not file_name.is_file():
        raise FileNotFoundError(f"File ({file_name}) does not exist ")

    return file_name
