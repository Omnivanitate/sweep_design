from typing import NamedTuple, Protocol, Tuple, runtime_checkable
import numpy as np

@runtime_checkable
class RelationProtocol(Protocol):
    def get_data(self) -> Tuple[np.ndarray, np.ndarray]: ...

class NotEqualError(Exception):
    def __init__(self, *args: object) -> None:
        message = f'Different size x_array({args[0]}) and y_array({args[1]})'
        super().__init__(message)

class BadInputError(Exception):
    pass

class ConvertingError(Exception):

    def __init__(self, *args: object) -> None:
        message = f'Can not convert type {args[0]} into type {args[1]}.'
        super().__init__(*args)

class TypeFuncError(Exception):

    def __init__(self, *args: object) -> None:
        message = f'operation "{args[0]}" did not complite with' \
            'type {args[1]} and type {args[2]}'
        super().__init__(message)

class BaseXY(NamedTuple):
    x: np.ndarray
    y: np.ndarray


class Spectrogram(NamedTuple):
    t: np.ndarray
    f: np.ndarray
    S: np.ndarray
