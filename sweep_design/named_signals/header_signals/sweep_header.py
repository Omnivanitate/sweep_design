from typing import Union, Callable

from .relation_header import HeaderRelation
from .signal_header import HeaderSignal
from .base_header import HeaderBase
from .defaults import names as dfn
from .defaults.methods import make_name, make_category

InName = Union[HeaderBase, str, Callable[[], str]]


class HeaderSweep(HeaderSignal):

    _quantity = 1
    _make_default_name = dfn.default_sweep_name

    def __init__(self, name: InName = None, category: str = None) -> None:

        if category is None:
            category = "sweep"

        super().__init__(name, category)

    def get_a_t(self, name: InName = None, category: str = None) -> HeaderRelation:
        if category is None:
            category = "a_t"
        name = make_name(name, dfn.make_default_a_t_name, self)
        category = make_category(self, category)
        return HeaderRelation(name, category)

    def get_f_t(self, name: InName = None, category: str = None) -> HeaderRelation:
        if category is None:
            category = "f_t"
        name = make_name(name, dfn.make_default_f_t_name, self)
        category = make_category(self, category)
        return HeaderRelation(name, category)

    def get_spectrogram(
        self, name: InName = None, category: str = None
    ) -> HeaderRelation:
        if category is None:
            category = "f_t"
        name = make_name(name, dfn.make_default_spectrogram_name, self)
        category = make_category(self, category)
        return HeaderRelation(name, category)


class HeaderSpectrogram(HeaderBase):

    _quantity = 1

    def __init__(self, name: InName = None, category: str = None) -> None:

        if category is None:
            category = "time_frequebcy"

        if name is None:
            name = dfn.make_spectrogram_name(HeaderSpectrogram._quantity)
            HeaderSpectrogram._quantity += 1

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

    def __str__(self) -> str:
        return self.name()

    def __repr__(self) -> str:
        return f"Name: {self.name()} category: {self.category}"
