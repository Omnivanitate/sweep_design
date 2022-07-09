from typing import Callable, Union, TypeVar

from .defaults import names as dfn
from .base_header import HeaderBase
from .relation_header import HeaderRelation
from .defaults.methods import make_name, make_category

InName = Union[HeaderBase, str, Callable[[], str]]
NSP = TypeVar("NSP", bound="HeaderSpectrum")


class HeaderSpectrum(HeaderRelation):

    _quantity = 1

    def __init__(self, name: InName = None, category: str = None) -> None:

        if category is None:
            category = "spectrum"

        if name is None:
            name = dfn.make_default_spectrum_name(HeaderSpectrum._quantity)
            HeaderSpectrum._quantity += 1

        super().__init__(name, category)

    def get_signal(self, name: InName = None, category: str = None) -> "HeaderSignal":
        name = make_name(name, dfn.make_default_spectrum2signal_name, self)
        return HeaderSignal(name, category)

    def get_amp_spectrum(
        self, name: InName = None, category: str = None
    ) -> "HeaderSpectrum":
        name = make_name(name, dfn.get_default_spectrum_name, self)
        category = make_category(self, category, dfn.make_default_amp_category_name)
        return HeaderSpectrum(name, category)

    def get_phase_spectrum(
        self, name: InName = None, category: str = None
    ) -> "HeaderSpectrum":
        name = make_name(name, dfn.get_default_spectrum_name, self)
        category = make_category(self, category, dfn.make_default_phase_category_name)
        return HeaderSpectrum(name, category)

    def get_reverse_filter(
        self, name: InName = None, category: str = None
    ) -> "HeaderSpectrum":
        name = make_name(name, dfn.make_default_name_reverse_filter, self)
        category = make_category(self, category)
        return HeaderSpectrum(name, category)

    def add_phase(
        self, other: HeaderBase, name: InName = None, category: str = None
    ) -> "HeaderSpectrum":
        name = make_name(name, dfn.make_default_add_phase_name, self, other)
        category = make_category(self, category)
        return HeaderSpectrum(name, category)

    def sub_phase(
        self, other: HeaderBase, name: InName = None, category: str = None
    ) -> "HeaderSpectrum":
        name = make_name(name, dfn.make_default_sub_phase_name, self, other)
        category = make_category(self, category)
        return HeaderSpectrum(name, category)

    @staticmethod
    def get_spectrum_from_amp_phase(
        amp: HeaderBase, phase: HeaderBase, name: InName = None, category="spectrum"
    ) -> "HeaderSpectrum":
        name = make_name(
            name, dfn.make_default_spectrum_from_amp_phase_name, amp, phase
        )
        return HeaderSpectrum(name, category)


class HeaderSignal(HeaderRelation):

    _quantity = 1
    _make_default_name = dfn.make_default_signal_name

    def __init__(self, name: InName = None, category: str = None) -> None:

        if category is None:
            category = "signal"

        super().__init__(name, category)

    def get_spectrum(
        self, name: InName = None, category="spectrum"
    ) -> "HeaderSpectrum":
        name = make_name(name, dfn.make_default_signal2spectrum_name, self)
        category = make_category(self, category)
        return HeaderSpectrum(name, category)

    def get_amlitude_spectrum(
        self, name: InName = None, category="amp_spectrum"
    ) -> "HeaderSpectrum":
        name = make_name(name, dfn.make_default_spectrum_from_amp_name, self)
        category = make_category(self, category)
        return HeaderSpectrum(name, category)

    def get_phase_spectrum(
        self, name: InName = None, category="phase_spectrum"
    ) -> "HeaderSpectrum":
        name = make_name(name, dfn.make_default_spectrum_from_phase_name, self)
        category = make_category(self, category)
        return HeaderSpectrum(name, category)

    def get_reverse_signal(
        self, name: InName = None, category: str = None
    ) -> "HeaderSignal":
        name = make_name(name, dfn.make_default_name_reverse_signal, self)
        category = make_category(self, category)
        return HeaderSignal(name, category)

    def add_phase(
        self, other: HeaderBase, name: InName = None, category: str = None
    ) -> "HeaderSignal":
        name = make_name(name, dfn.make_default_add_phase_name, self, other)
        category = make_category(self, category)
        return HeaderSignal(name, category)

    def sub_phase(
        self, other: HeaderBase, name: InName = None, category: str = None
    ) -> "HeaderSignal":
        name = make_name(name, dfn.make_default_sub_phase_name, self, other)
        category = make_category(self, category)
        return HeaderSignal(name, category)
