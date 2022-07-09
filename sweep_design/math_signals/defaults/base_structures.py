from typing import NamedTuple, Protocol, Tuple, runtime_checkable
import numpy as np
from enum import Enum


class NotEqualError(Exception):
    def __init__(self, *args: object) -> None:
        message = f"Different size x_array({args[0]}) and y_array({args[1]})"
        super().__init__(message)


class BadInputError(Exception):
    pass


class ConvertingError(Exception):
    def __init__(self, *args: object) -> None:
        message = f"Can not convert type {args[0]} into type {args[1]}."
        super().__init__(message)


class TypeFuncError(Exception):
    def __init__(self, *args: object) -> None:
        message = f'operation "{args[0]}" did not complite with type {args[1]} and type {args[2]}'
        super().__init__(message)


@runtime_checkable
class RelationProtocol(Protocol):
    @property
    def x(self) -> np.ndarray:
        ...

    @property
    def y(self) -> np.ndarray:
        ...

    def get_data(self) -> Tuple[np.ndarray, np.ndarray]:
        ...


class MathOperation(Enum):
    ADD = "__add__"
    RADD = "__radd__"
    SUB = "__sub__"
    RSUB = "__rsub__"
    MUL = "__mul__"
    RMUL = "__rmul__"
    TRUEDIV = "__truediv__"
    RTRUEDIV = "__rtruediv__"
    POW = "__pow__"
    RPOW = "__rpow__"


class BaseXY(NamedTuple):
    x: np.ndarray
    y: np.ndarray


class Spectrogram(NamedTuple):
    time: np.ndarray
    frequency: np.ndarray
    spectrogram_matrix: np.ndarray
