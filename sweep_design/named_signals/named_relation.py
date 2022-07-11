from typing import Any, Callable, Optional, Tuple, Type, TypeVar, Union

import numpy as np

from ..config.named_config import NamedConfig
from ..math_signals.defaults.base_structures import MathOperation
from ..math_signals.math_relation import Relation
from .header_signals.base_header import HeaderBase
from .header_signals.relation_header import HeaderRelation

Num = Union[float, int, complex]
CR = TypeVar("CR", bound="NamedRelation")
CR2 = TypeVar("CR2", bound="NamedRelation")
InName = Union[HeaderBase, str, Callable[[], str]]
InData = Union[CR, Relation]
Any = Union[InData, Num]
T = TypeVar("T")

default_name_composed_relation = "DR"


class NamedRelation:

    extract_input_default = NamedConfig.extract_input

    def __init__(
        self, x: Any, y: Any = None, name: InName = None, category: str = None
    ) -> None:

        x, y = NamedConfig.extract_input(x, y)

        if category is None:
            category = "relation"

        self._relation = Relation(x, y)
        self.header = HeaderRelation(name, category)

    @property
    def x(self):
        return self._relation.x

    @property
    def y(self):
        return self._relation.y

    @property
    def dx(self):
        return self._relation.dx

    @property
    def relation(self):
        return self._relation

    @property
    def category(self):
        return self.header.category

    @classmethod
    def _convert_input(
        cls: Type[CR], data: Any, name: InName = None
    ) -> "NamedRelation":
        if not isinstance(data, NamedRelation):
            if not name:
                name = default_name_composed_relation
            return NamedRelation(cls.extract_input_default(data, None), name=name)
        return data

    def _operate(
        self: CR,
        other: Any,
        operation: MathOperation,
        name: Optional[InName],
        category: Optional[str],
    ) -> CR:

        if not isinstance(other, (NamedRelation, float, int, complex)):
            other = self._convert_input(other)

        relation = getattr(self._relation, operation.value)(other)
        header = getattr(self.header, operation.value)(other, name, category)
        return type(self)(relation, name=header)

    def get_data(self) -> Tuple[np.ndarray, np.ndarray]:
        return self._relation.get_data()

    def select_data(
        self: CR,
        x_start: Num = None,
        x_end: Num = None,
        name: InName = None,
        category: str = None,
    ) -> CR:

        if x_start is None:
            x_start = self._relation._x[0]

        if x_end is None:
            x_end = self._relation._x[-1]

        header = self.header.select_data(x_start, x_end, name, category)
        relation = self._relation.select_data(x_start, x_end)
        return type(self)(relation, name=header)

    def exp(self: CR, name: InName = None, category="relation") -> CR:
        header = self.header.exp(name, category)
        relation = self._relation.exp()
        return type(self)(relation, name=header)

    def diff(self: CR, name: InName = None, category="relation") -> CR:
        header = self.header.diff(name=name, category=category)
        relation = self._relation.diff()
        return type(self)(relation, name=header)

    def integrate(self: CR, name: InName = None, category="relation") -> CR:
        header = self.header.integrate(name, category)
        relation = self._relation.integrate()
        return type(self)(relation, name=header)

    def interpolate_extrapolate(
        self: CR, new_x, name: InName = None, category="relation"
    ) -> CR:
        header = self.header.interpolate_extrapolate(new_x, name, category)
        relation = self._relation.interpolate_extrapolate(new_x)
        return type(self)(relation, name=header)

    def shift(
        self: CR, x_shift: Num = 0.0, name: InName = None, category="relation"
    ) -> CR:
        header = self.header.shift(x_shift, name, category)
        relation = self._relation.shift(x_shift)
        return type(self)(relation, name=header)

    @classmethod
    def equalize(
        cls: Type[CR],
        cr1: Any,
        cr2: Any,
        name1: InName = None,
        name2: InName = None,
        category1: str = None,
        category2: str = None,
    ) -> Tuple[CR, CR2]:
        cr1 = cls._convert_input(cr1)
        cr2 = cls._convert_input(cr2)
        r1, r2 = Relation.equalize(cr1.relation, cr2.relation)
        header1, header2 = HeaderRelation.equalize(
            cr1.header, cr2.header, r1, name1, name2, category1, category2
        )
        return type(cr1)(r1, name=header1), type(cr2)(r2, name=header2)

    @classmethod
    def convolve(
        cls: Type[CR],
        cr1: Any,
        cr2: Any,
        name: InName = None,
        category: str = "relation",
    ) -> CR:
        cr1 = cls._convert_input(cr1)
        cr2 = cls._convert_input(cr2)
        relation = Relation.convolve(cr1.relation, cr2.relation)
        header = HeaderRelation.convolve(cr1.header, cr2.header, name, category)
        return cls(relation, name=header)

    @classmethod
    def correlate(
        cls: Type[CR],
        cr1: Any,
        cr2: Any,
        name: InName = None,
        category: str = "relation",
    ) -> CR:
        cr1 = cls._convert_input(cr1)
        cr2 = cls._convert_input(cr2)
        named = HeaderRelation.convolve(cr1.header, cr2.header, name, category)
        relation = Relation.correlate(cr1.relation, cr2.relation)
        return cls(relation, name=named)

    def __str__(self) -> str:
        return str(self.header)

    def __add__(self: CR, other: Any, name: InName = None, category="relation") -> CR:
        return self._operate(other, MathOperation.ADD, name, category)

    def __radd__(self: CR, other: Any, name: InName = None, category="relation") -> CR:
        return self._operate(other, MathOperation.RADD, name, category)

    def __sub__(self: CR, other: Any, name: InName = None, category="relation") -> CR:
        return self._operate(other, MathOperation.SUB, name, category)

    def __rsub__(self: CR, other: Any, name: InName = None, category="relation") -> CR:
        return self._operate(other, MathOperation.RSUB, name, category)

    def __mul__(self: CR, other: Any, name: InName = None, category="relation") -> CR:
        return self._operate(other, MathOperation.MUL, name, category)

    def __rmul__(self: CR, other: Any, name: InName = None, category="relation") -> CR:
        return self._operate(other, MathOperation.RMUL, name, category)

    def __truediv__(
        self: CR, other: Any, name: InName = None, category="relation"
    ) -> CR:
        return self._operate(other, MathOperation.TRUEDIV, name, category)

    def __rtruediv__(
        self: CR, other: Any, name: InName = None, category="relation"
    ) -> CR:
        return self._operate(other, MathOperation.RTRUEDIV, name, category)

    def __pow__(self: CR, other: Any, name: InName = None, category="relation") -> CR:
        return self._operate(other, MathOperation.POW, name, category)

    def __rpow__(self: CR, other: Any, name: InName = None, category="relation") -> CR:
        return self._operate(other, MathOperation.RPOW, name, category)

    def __iadd__(self: CR, other: Any, name: InName = None, category="relation") -> CR:
        return self.__add__(other, name, category)

    def __isub__(self: CR, other: Any, name: InName = None, category="relation") -> CR:
        return self.__sub__(other, name, category)

    def __imul__(self: CR, other: Any, name: InName = None, category="relation") -> CR:
        return self.__mul__(other, name, category)

    def __idiv__(self: CR, other: Any, name: InName = None, category="relation") -> CR:
        return self.__truediv__(other, name, category)

    def __ipow__(self: CR, other: Any, name: InName = None, category="relation") -> CR:
        return self.__pow__(other, name, category)

    def __getitem__(self, item: Union[float, slice]):
        if isinstance(item, float):
            x = self._relation._x 
            idx = (np.abs(x - item)).argmin()
            return x[idx], self._relation._y[idx]
        if isinstance(item, slice):
            return self.select_data(item.start, item.stop)