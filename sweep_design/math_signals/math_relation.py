import logging
from typing import Tuple, Type, TypeVar, Union

import numpy as np
from numpy.typing import NDArray

from ..config import Config
from .defaults.base_structures import (
    BadInputError,
    MathOperation,
    NotEqualError,
    RelationProtocol,
    TypeFuncError,
)

Num = Union[float, int, complex]
R = TypeVar("R", bound="Relation")
R2 = TypeVar("R2", bound="Relation")


class Relation:
    """A representation of dependency y from x (y = f(x))

    The class describe a dependency between two sequences x, y,
    represented by real or complex numbers. The length of sequences must be
    the same, and the sampling rate must not change throughout the entire
    sequence.

    **Properties**:
    > **x**: `Union[RelationProtocol, NDArray]`
    The Relation class, or a class derived from the Relation class, or
    an array_like object containing numbers(real or complex).

    > **y**: `NDArray` = None.
    None or array_like object containing real or complex numbers.

    > **dx**: `float` = None.
    Sample rate x-axis.

    For the instance of `Relation` class, define the basic mathematical operstions:
    *additon (+), subtraction(-), multiplication('*'), devision(/),
    expopnentiation ('*''*') and their unary representation (+=, -=, *=, /=).
    The result of the operation is a new instance of the Relation class.

    Determined correlation and convolution between two instances
    (methods: correlate and convolve).

    How those operations will be calculated determined by the methods described
    in the Config class. Methods can be overridden if necessary
    (sweep_design.math_signals.config).

    WARNING!!! When inheriting the Relation class, it is important to write correctly
    constructor. It must match the constructor of the Relation class.
    Because some methods return a type(self)(...). For example,
    addition method (def __add__(self: R, other: Union['Relation', Num])
     -> R). Or predefine these methods in the inherited class.

    """

    def __init__(
        self,
        x: Union[RelationProtocol, NDArray],
        y: NDArray = None,
        dx: float = None,
        **kwargs,
    ) -> None:

        self._math_operation = Config.math_operation
        self._interpolate_extrapolate_method = Config.interpolate_extrapolate_method
        self._integrate_one_method = Config.integrate_one_method
        self._integrate_method = Config.integrate_method
        self._differentiate_method = Config.differentiate_method

        self._dx = dx

        if isinstance(x, RelationProtocol):
            self._x, self._y = x.get_data()
            if y is not None:
                logging.warning(f'x is instance of {type(x)}, "y" was ignored')
        else:
            if y is None:
                raise BadInputError("y absent. Not enough data!")

            if Config.CONVERT2ARRAY:
                x, y = np.array(x), np.array(y)

            if x.size != y.size:
                raise NotEqualError(x.size, y.size)

            self._x, self._y = x, y

    @property
    def x(self) -> np.ndarray:
        return self._x.copy()

    @property
    def dx(self) -> float:
        if self._dx is not None:
            return self._dx
        diff_x = np.diff(self._x)
        values, counts = np.unique(diff_x, return_counts=True)

        num = values[np.argmax(counts)]
        if num < 1:
            self._dx = 1 / round(1 / num)
        else:
            self._dx = round(num)
        return self._dx

    @dx.setter
    def dx(self, value: float) -> None:
        self._dx = value

    @property
    def y(self) -> np.ndarray:
        return self._y.copy()

    def get_data(self) -> Tuple[np.ndarray, np.ndarray]:
        """Return the data of the called object."""
        return self._x.copy(), self._y.copy()

    def max(self) -> Num:
        return self._y.max()

    def min(self) -> Num:
        return self._y.min()

    def get_norm(self) -> float:
        """Get signal rate.

        Calculated in terms of signal energy.
        """
        x, y = self._x, self._y
        return self._integrate_one_method(y**2, x) / (self.dx)

    def select_data(self: R, x_start: Num = None, x_end: Num = None, **kwargs) -> R:
        """Select data using x-axis."""

        x, y = self.get_data()

        if x_start is None:
            x_start = x[0]

        if x_end is None:
            x_end = x[-1]

        is_selected = np.logical_and(
            np.greater_equal(self._x, x_start), np.less_equal(self._x, x_end)
        )

        return type(self)(x[is_selected], y[is_selected], **kwargs)

    def exp(self: R, **kwargs) -> R:
        x, y = self.get_data()
        return type(self)(x, np.exp(y), **kwargs)

    def diff(self: R, **kwargs) -> R:
        x, y = self.get_data()
        result = self._differentiate_method(x, y, self.dx)
        return type(self)(*result, **kwargs)

    def integrate(self: R, **kwargs) -> R:
        x, y = self.get_data()
        result = self._integrate_method(x, y, self.dx)
        return type(self)(*result, **kwargs)

    def interpolate_extrapolate(self: R, new_x: np.ndarray, **kwargs) -> R:
        new_y = self._interpolate_extrapolate_method(self._x, self._y)(new_x)
        return type(self)(new_x, new_y, **kwargs)

    def shift(self: R, x_shift: Num = 0, **kwargs) -> R:
        x, y = self.get_data()
        return type(self)(x + x_shift, y, **kwargs)

    @staticmethod
    def equalize(r1: R, r2: R2) -> Tuple[R, R2]:
        x1, _ = r1.get_data()
        x2, _ = r2.get_data()
        comparation = x1 == x2
        if isinstance(comparation, np.ndarray):
            if all(comparation):
                return r1, r2
        x_new = Config.get_common_x(x1, x2, r1.dx, r2.dx)
        r1 = r1.interpolate_extrapolate(x_new)
        r2 = r2.interpolate_extrapolate(x_new)
        return r1, r2

    @classmethod
    def correlate(cls: Type[R], r1: "Relation", r2: "Relation", **kwargs) -> R:

        if isinstance(r1, Relation) and isinstance(r2, Relation):
            result = Config.correlate_method(cls, r1, r2)
            return cls(*result, **kwargs)
        else:
            raise TypeFuncError("Correlation", type(r1), type(r2))

    @classmethod
    def convolve(cls: Type[R], r1: "Relation", r2: "Relation", **kwargs) -> R:

        if isinstance(r1, Relation) and isinstance(r2, Relation):
            result = Config.convolve_method(cls, r1, r2)
            return cls(*result, **kwargs)
        else:
            raise TypeFuncError("Convolution", type(r1), type(r2))

    @staticmethod
    def _operation(
        a: "Relation", b: Union["Relation", Num], name_operation: MathOperation
    ) -> Tuple[np.ndarray, np.ndarray]:
        logging.debug(f"Type of a: {type(a)}")
        logging.debug(f"Type of b: {type(b)}")
        if isinstance(b, RelationProtocol):
            r1, r2 = Relation.equalize(a, b)
            x, y1 = r1.get_data()
            _, y2 = r2.get_data()
            return a._math_operation(x, y1, y2, name_operation)
        elif isinstance(b, (float, int, complex)):
            x, y = a.get_data()
            return a._math_operation(x, y, b, name_operation)
        else:
            raise TypeFuncError(name_operation.value.strip("_"), type(a), type(b))

    def __add__(self: R, other: Union["Relation", Num], **kwargs) -> R:
        return type(self)(*self._operation(self, other, MathOperation.ADD), **kwargs)

    def __radd__(self: R, other: Union["Relation", Num], **kwargs) -> R:
        return type(self)(*self._operation(self, other, MathOperation.RADD), **kwargs)

    def __sub__(self: R, other: Union["Relation", Num], **kwargs) -> R:
        return type(self)(*self._operation(self, other, MathOperation.SUB), **kwargs)

    def __rsub__(self: R, other: Union["Relation", Num], **kwargs) -> R:
        return type(self)(*self._operation(self, other, MathOperation.RSUB), **kwargs)

    def __mul__(self: R, other: Union["Relation", Num], **kwargs) -> R:
        return type(self)(*self._operation(self, other, MathOperation.MUL), **kwargs)

    def __rmul__(self: R, other: Union["Relation", Num], **kwargs) -> R:
        return type(self)(*self._operation(self, other, MathOperation.RMUL), **kwargs)

    def __truediv__(self: R, other: Union["Relation", Num], **kwargs) -> R:
        return type(self)(
            *self._operation(self, other, MathOperation.TRUEDIV), **kwargs
        )

    def __rtruediv__(self: R, other: Union["Relation", Num], **kwargs) -> R:
        return type(self)(
            *self._operation(self, other, MathOperation.RTRUEDIV), **kwargs
        )

    def __pow__(self: R, other: Union["Relation", Num], **kwargs) -> R:
        return type(self)(*self._operation(self, other, MathOperation.POW), **kwargs)

    def __rpow__(self: R, other: Union["Relation", Num], **kwargs) -> R:
        return type(self)(*self._operation(self, other, MathOperation.RPOW), **kwargs)

    def __iadd__(self: R, other: Union["Relation", Num], **kwargs) -> R:
        return self.__add__(other, **kwargs)

    def __isub__(self: R, other: Union["Relation", Num], **kwargs) -> R:
        return self.__sub__(other, **kwargs)

    def __imul__(self: R, other: Union["Relation", Num], **kwargs) -> R:
        return self.__mul__(other, **kwargs)

    def __idiv__(self: R, other: Union["Relation", Num], **kwargs) -> R:
        return self.__truediv__(other, **kwargs)

    def __ipow__(self: R, other: Union["Relation", Num], **kwargs) -> R:
        return self.__pow__(other, **kwargs)

    def __len__(self) -> int:
        return self._x.size

    def __getitem__(self, item: Union[float, slice]):
        if isinstance(item, float):
            idx = (np.abs(self._x - item)).argmin()
            return self._x[idx], self._y[idx]
        if isinstance(item, slice):
            return self.select_data(item.start, item.stop)
