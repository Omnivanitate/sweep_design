from typing import Any, Callable, Optional, Type, TypeVar, Union

from ..math_signals.math_relation import Relation
from ..math_signals.math_signal import Signal, Spectrum
from .header_signals.base_header import HeaderBase
from .header_signals.signal_header import HeaderSignal, HeaderSpectrum
from .named_relation import NamedRelation
from ..config.named_config import NamedConfig

Num = Union[float, int, complex]
CR = TypeVar("CR", bound="NamedRelation")
InName = Union[HeaderBase, str, Callable[[], str]]
InData = Union[NamedRelation, "NamedSignal", "NamedSpectrum"]
InDataN = Union[NamedRelation, Relation, HeaderBase, Num]
CSP = TypeVar("CSP", bound="NamedSpectrum")
CS = TypeVar("CS", bound="NamedSignal")


class NamedSpectrum(NamedRelation):
    def __init__(
        self, f: Any, s_a: Any = None, name: InName = None, category="spectrum"
    ) -> None:
        f, s_a = NamedConfig.extract_input(f, s_a)
        self._relation: Spectrum = Spectrum(f, s_a)
        self.header: HeaderSpectrum = HeaderSpectrum(name=name, category=category)
        self.signal: Optional[NamedSignal] = None

    def get_signal(
        self,
        recalculate=False,
        start_time: float = None,
        name: InName = None,
        category: str = None,
    ) -> "NamedSignal":

        if self.signal is None or recalculate:
            signal = self._relation.get_signal(
                recalculate=recalculate, start_time=start_time
            )
            header = self.header.get_signal(name, category)
            self.signal = NamedSignal(signal, name=header)
        return self.signal

    def get_amp_spectrum(
        self, name: InName = None, category: str = "amp_spectrum"
    ) -> NamedRelation:
        relation = self._relation.get_amp_spectrum()
        header = self.header.get_amp_spectrum(name, category)
        return NamedRelation(relation, name=header)

    def get_phase_spectrum(
        self, name: InName = None, category: str = "phase_spectrum"
    ) -> NamedRelation:
        relation = self._relation.get_phase_spectrum()
        header = self.header.get_phase_spectrum(name, category)
        return NamedRelation(relation, name=header)

    def get_reverse_filter(
        self: CSP,
        percent: Union[float, int] = 5,
        subtrack_phase=True,
        f_start: float = None,
        f_end: float = None,
        name: InName = None,
        category: str = None,
    ) -> CSP:
        header = self.header.get_reverse_filter(name, category)
        spectrum = self._relation.get_reverse_filter(
            percent=percent,
            subtrack_phase=subtrack_phase,
            f_start=f_start,
            f_end=f_end,
            name=header,
        )
        return type(self)(spectrum, name=header)

    def add_phase(
        self: CSP, other: Any, name: InName = None, category: str = None
    ) -> CSP:
        c_other = super()._convert_input(other)
        header = self.header.add_phase(c_other.header, name, category)
        spectrum = self._relation.add_phase(c_other.relation, name=header)
        return type(self)(spectrum, name=header)

    def sub_phase(
        self: CSP, other: Any, name: InName = None, category: str = None
    ) -> CSP:
        c_other = super()._convert_input(other)
        header = self.header.sub_phase(c_other.header, name, category)
        spectrum = self._relation.add_phase(c_other.relation, name=header)
        return type(self)(spectrum, name=header)

    @classmethod
    def get_spectrum_from_amp_phase(
        cls: Type[CSP],
        r1: Any,
        r2: Any,
        name: InName = None,
        category="spectrum",
    ) -> CSP:
        c_r1 = super()._convert_input(r1)
        c_r2 = super()._convert_input(r2)
        header = HeaderSpectrum.get_spectrum_from_amp_phase(
            c_r1.header, c_r2.header, name, category
        )
        spectrum = Spectrum.get_spectrum_from_amp_phase(c_r1.relation, c_r2.relation)
        return cls(spectrum, name=header)


class NamedSignal(NamedRelation):
    def __init__(
        self, t: Any, a: Any = None, name: InName = None, category="signal"
    ) -> None:
        t, a = NamedConfig.extract_input(t, a)
        self._relation: Signal = Signal(t, a)
        self.header: HeaderSignal = HeaderSignal(name, category)
        self.spectrum: Optional[NamedSpectrum] = None

    def get_amplitude_spectrum(
        self,
        recalculate=False,
        is_start_zero=False,
        name: InName = None,
        category: str = None,
    ) -> NamedRelation:

        amplitude_spectrum = self._relation.get_amplitude_spectrum(
            recalculate=recalculate, is_start_zero=is_start_zero
        )
        header = self.header.get_amlitude_spectrum(name, category)
        return NamedRelation(amplitude_spectrum, name=header)

    def get_phase_spectrum(
        self,
        recalculate=False,
        is_start_zero=False,
        name: InName = None,
        category: str = None,
    ) -> NamedRelation:

        phase_spectrum = self._relation.get_phase_spectrum(
            recalculate=recalculate, is_start_zero=is_start_zero
        )
        header = self.header.get_phase_spectrum(name, category)
        return NamedRelation(phase_spectrum, name=header)

    def get_spectrum(
        self,
        recalculate=False,
        is_start_zero=False,
        name: InName = None,
        category: str = None,
    ) -> NamedSpectrum:
        if self.spectrum is None or recalculate:
            spectrum = self._relation.get_spectrum(
                recalculate=recalculate, is_start_zero=is_start_zero
            )
            header = self.header.get_spectrum(name, category)
            self.spectrum = NamedSpectrum(spectrum, name=header)
        return self.spectrum

    def get_reverse_signal(
        self: CS,
        percent: Union[float, int] = 5,
        subtrack_phase: bool = True,
        f_start: float = None,
        f_end: float = None,
        name: InName = None,
        category: str = None,
    ) -> CS:
        header = self.header.get_reverse_signal(name, category)
        signal = self._relation.get_reverse_signal(
            percent=percent,
            subtrack_phase=subtrack_phase,
            f_start=f_start,
            f_end=f_end,
        )
        return type(self)(signal, name=header)

    def add_phase(
        self: CS, other: Any, name: InName = None, category: str = None
    ) -> CS:
        r_other = super()._convert_input(other)
        header = self.header.add_phase(r_other.header, name, category)
        signal = self._relation.add_phase(r_other.relation)
        return type(self)(signal, name=header)

    def sub_phase(
        self: CS, other: Any, name: InName = None, category: str = None
    ) -> CS:
        r_other = super()._convert_input(other)
        header = self.header.sub_phase(r_other.header, name, category)
        signal = self._relation.sub_phase(r_other.relation)
        return type(self)(signal, name=header)
