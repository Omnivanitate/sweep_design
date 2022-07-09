import inspect
from typing import Optional, Tuple, Type, TypeVar, Union, Callable

import numpy as np

from ...math_signals.math_relation import Relation
from ...math_signals.defaults.base_structures import TypeFuncError
from ...math_signals.defaults.base_structures import MathOperation
from .base_header import HeaderBase
from .defaults import names as dfn
from .defaults.methods import make_name, make_category
from ...config.named_config import NamedConfig

Num = Union[float, int, complex]
InName = Union[HeaderBase, str, Callable[[], str]]
NR = TypeVar("NR", bound="HeaderRelation")


class BadNameCategory(Exception):
    pass


def _get_name_by_trace(position: int) -> str:
    frames_callers = inspect.stack()
    for n, k in enumerate(frames_callers):
        if "IPython" in k.filename:
            break

        names = frames_callers[n].frame.f_code.co_names
        if len(names) > 2:
            name = names[position]
        else:
            name = names[-1]
    return name


def set_name_by_trace(name: Optional[str], is_set=False, position=-1):
    if name is None:
        if is_set:
            name = _get_name_by_trace(position)
    return name


class HeaderRelation(HeaderBase):

    _quantity = 1
    _make_default_name = dfn.make_default_relation_name

    def __init__(
        self, name: InName = None, category: Optional[str] = "relation", **kwargs
    ) -> None:

        if name is None:
            if not NamedConfig.NAMING_BY_ASSIGNMENT_CREATE:
                name = type(self)._make_default_name(HeaderRelation._quantity)
                type(self)._quantity += 1
            else:
                name = _get_name_by_trace(-1)
        if category is None:
            category = "relation"

        super().__init__(name, category)

    @property
    def category(self) -> str:
        return self._category

    @category.setter
    def category(self, value) -> None:
        self._category = value

    @property
    def name(self) -> Callable[..., str]:
        return self._name

    @name.setter
    def name(self, value: InName) -> None:
        if callable(value) and isinstance(value(), str):
            self._name = value
        elif isinstance(value, HeaderBase):
            self._name = value._name
        else:
            str(value)

            def call() -> str:
                return str(value)

            self._name = call

    def select_data(
        self,
        x_start: Num,
        x_end: Num,
        name: InName = None,
        category="relation",
        **kwargs,
    ) -> "HeaderRelation":

        name = set_name_by_trace(name, NamedConfig.NAMING_BY_ASSIGNMENT_OTHER_OPERATION)
        name = make_name(name, dfn.make_default_name_select_data, self, x_start, x_end)
        category = make_category(self, category)
        return HeaderRelation(name, category, **kwargs)

    def exp(self, name: InName = None, category: str = None) -> "HeaderRelation":

        name = set_name_by_trace(name, NamedConfig.NAMING_BY_ASSIGNMENT_OTHER_OPERATION)
        name = make_name(name, dfn.make_default_name_exp, self)
        category = make_category(self, category)
        return HeaderRelation(name, category)

    def diff(self, name: InName = None, category: str = None) -> "HeaderRelation":

        name = set_name_by_trace(name, NamedConfig.NAMING_BY_ASSIGNMENT_OTHER_OPERATION)
        name = make_name(name, dfn.make_default_diff_name, self)
        category = make_category(self, category, dfn.make_diff_category_name)
        return HeaderRelation(name, category)

    def integrate(self, name: InName = None, category: str = None) -> "HeaderRelation":

        name = set_name_by_trace(name, NamedConfig.NAMING_BY_ASSIGNMENT_OTHER_OPERATION)
        name = make_name(name, dfn.make_default_integrate_name, self)
        category = make_category(self, category, dfn.make_integrate_category_name)
        return HeaderRelation(name, category)

    def interpolate_extrapolate(
        self,
        new_x: Union[np.ndarray, Relation],
        name: InName = None,
        category: str = None,
    ) -> "HeaderRelation":
        if isinstance(new_x, Relation):
            new_x, _ = new_x.get_data()
        name = set_name_by_trace(name, NamedConfig.NAMING_BY_ASSIGNMENT_OTHER_OPERATION)
        name = make_name(name, dfn.make_default_interpolate_name, self, new_x)
        category = make_category(self, category)
        return HeaderRelation(name, category)

    def shift(
        self, x_shift: Num, name: InName = None, category: str = None
    ) -> "HeaderRelation":

        name = set_name_by_trace(name, NamedConfig.NAMING_BY_ASSIGNMENT_OTHER_OPERATION)
        name = make_name(name, dfn.make_default_shift_name, self, x_shift)
        category = make_category(self, category)
        return HeaderRelation(name, category)

    @staticmethod
    def equalize(
        r1: "HeaderRelation",
        r2: "HeaderRelation",
        new_x: Union[Relation, np.ndarray],
        name1: InName = None,
        name2: InName = None,
        category1: str = None,
        category2: str = None,
    ) -> Tuple[HeaderBase, HeaderBase]:
        name1 = set_name_by_trace(
            name1, NamedConfig.NAMING_BY_ASSIGNMENT_OTHER_OPERATION, -2
        )
        name2 = set_name_by_trace(
            name2, NamedConfig.NAMING_BY_ASSIGNMENT_OTHER_OPERATION, -1
        )
        r1 = r1.interpolate_extrapolate(new_x, name1, category1)
        r2 = r2.interpolate_extrapolate(new_x, name2, category2)
        return r1, r2

    @classmethod
    def correlate(
        cls: Type["HeaderRelation"],
        r1: "HeaderRelation",
        r2: "HeaderRelation",
        name: InName = None,
        category=None,
        **kwargs,
    ) -> "HeaderRelation":

        if isinstance(r1, HeaderRelation) and isinstance(r2, HeaderRelation):
            name = set_name_by_trace(
                name, NamedConfig.NAMING_BY_ASSIGNMENT_OTHER_OPERATION
            )
            name = make_name(name, dfn.make_default_name_correlation, r1, r2)
            category = make_category(r1, category)
            return cls(name, category)
        else:
            raise TypeFuncError("Correlation", type(r1), type(r2))

    @classmethod
    def convolve(
        cls: Type["HeaderRelation"],
        r1: "HeaderRelation",
        r2: "HeaderRelation",
        name: InName = None,
        category: str = None,
        **kwargs,
    ) -> "HeaderRelation":

        if isinstance(r1, HeaderRelation) and isinstance(r2, HeaderRelation):
            name = set_name_by_trace(
                name, NamedConfig.NAMING_BY_ASSIGNMENT_OTHER_OPERATION
            )
            name = make_name(name, dfn.make_default_name_convolution, r1, r2)
            category = make_category(r1, category)
            return cls(name, category)
        else:
            raise TypeFuncError("Convolution", type(r1), type(r2))

    def __str__(self) -> str:
        return self.name()

    def __repr__(self) -> str:
        return f"Name: {self.name()} category: {self.category}"

    def __add__(
        self,
        other: Union["HeaderRelation", Num],
        name: InName = None,
        category: str = None,
    ) -> "HeaderRelation":

        name = set_name_by_trace(name, NamedConfig.NAMING_BY_ASSIGNMENT_MATH_OPERATION)
        name = make_name(
            name, dfn.make_default_names_operations, self, other, MathOperation.ADD
        )
        category = make_category(self, category)
        return HeaderRelation(name, category)

    def __radd__(
        self,
        other: Union["HeaderRelation", Num],
        name: InName = None,
        category: str = None,
    ) -> "HeaderRelation":

        name = set_name_by_trace(name, NamedConfig.NAMING_BY_ASSIGNMENT_MATH_OPERATION)
        name = make_name(
            name, dfn.make_default_names_operations, self, other, MathOperation.RADD
        )
        category = make_category(self, category)
        return HeaderRelation(name, category)

    def __sub__(
        self,
        other: Union["HeaderRelation", Num],
        name: InName = None,
        category: str = None,
    ) -> "HeaderRelation":

        name = set_name_by_trace(name, NamedConfig.NAMING_BY_ASSIGNMENT_MATH_OPERATION)
        name = make_name(
            name, dfn.make_default_names_operations, self, other, MathOperation.SUB
        )
        category = make_category(self, category)
        return HeaderRelation(name, category)

    def __rsub__(
        self,
        other: Union["HeaderRelation", Num],
        name: InName = None,
        category: str = None,
    ) -> "HeaderRelation":

        name = set_name_by_trace(name, NamedConfig.NAMING_BY_ASSIGNMENT_MATH_OPERATION)
        name = make_name(
            name, dfn.make_default_names_operations, self, other, MathOperation.RSUB
        )
        category = make_category(self, category)
        return HeaderRelation(name, category)

    def __mul__(
        self,
        other: Union["HeaderRelation", Num],
        name: InName = None,
        category: str = None,
    ) -> "HeaderRelation":

        name = set_name_by_trace(name, NamedConfig.NAMING_BY_ASSIGNMENT_MATH_OPERATION)
        name = make_name(
            name, dfn.make_default_names_operations, self, other, MathOperation.MUL
        )
        category = make_category(self, category)
        return HeaderRelation(name, category)

    def __rmul__(
        self,
        other: Union["HeaderRelation", Num],
        name: InName = None,
        category: str = None,
    ) -> "HeaderRelation":

        name = set_name_by_trace(name, NamedConfig.NAMING_BY_ASSIGNMENT_MATH_OPERATION)
        name = make_name(
            name, dfn.make_default_names_operations, self, other, MathOperation.RMUL
        )
        category = make_category(self, category)
        return HeaderRelation(name, category)

    def __truediv__(
        self,
        other: Union["HeaderRelation", Num],
        name: InName = None,
        category: str = None,
    ) -> "HeaderRelation":

        name = set_name_by_trace(name, NamedConfig.NAMING_BY_ASSIGNMENT_MATH_OPERATION)
        name = make_name(
            name, dfn.make_default_names_operations, self, other, MathOperation.TRUEDIV
        )
        category = make_category(self, category)
        return HeaderRelation(name, category)

    def __rtruediv__(
        self,
        other: Union["HeaderRelation", Num],
        name: InName = None,
        category: str = None,
    ) -> "HeaderRelation":

        name = set_name_by_trace(name, NamedConfig.NAMING_BY_ASSIGNMENT_MATH_OPERATION)
        name = make_name(
            name, dfn.make_default_names_operations, self, other, MathOperation.RTRUEDIV
        )
        category = make_category(self, category)
        return HeaderRelation(name, category)

    def __pow__(
        self,
        other: Union["HeaderRelation", Num],
        name: InName = None,
        category: str = None,
    ) -> "HeaderRelation":

        name = set_name_by_trace(name, NamedConfig.NAMING_BY_ASSIGNMENT_MATH_OPERATION)
        name = make_name(
            name, dfn.make_default_names_operations, self, other, MathOperation.POW
        )
        category = make_category(self, category)
        return HeaderRelation(name, category)

    def __rpow__(
        self,
        other: Union["HeaderRelation", Num],
        name: InName = None,
        category: str = None,
    ) -> "HeaderRelation":

        name = set_name_by_trace(name, NamedConfig.NAMING_BY_ASSIGNMENT_MATH_OPERATION)
        name = make_name(
            name, dfn.make_default_names_operations, self, other, MathOperation.RPOW
        )
        category = make_category(self, category)
        return HeaderRelation(name, category)

    def __iadd__(
        self,
        other: Union["HeaderRelation", Num],
        name: InName = None,
        category: str = None,
    ) -> "HeaderRelation":
        return self.__add__(other, name, category)

    def __isub__(
        self,
        other: Union["HeaderRelation", Num],
        name: InName = None,
        category: str = None,
    ) -> "HeaderRelation":
        return self.__sub__(other, name, category)

    def __imul__(
        self,
        other: Union["HeaderRelation", Num],
        name: InName = None,
        category: str = None,
    ) -> "HeaderRelation":
        return self.__mul__(other, name, category)

    def __idiv__(
        self,
        other: Union["HeaderRelation", Num],
        name: InName = None,
        category: str = None,
    ) -> "HeaderRelation":
        return self.__truediv__(other, name, category)

    def __ipow__(
        self,
        other: Union["HeaderRelation", Num],
        name: InName = None,
        category: str = None,
    ) -> "HeaderRelation":
        return self.__pow__(other, name, category)
