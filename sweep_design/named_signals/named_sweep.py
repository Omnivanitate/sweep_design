from typing import Any, Union, Callable, Optional

from sweep_design.config.named_config import NamedConfig

from .named_relation import NamedRelation

from .header_signals.base_header import HeaderBase
from .header_signals.sweep_header import HeaderSpectrogram, HeaderSweep
from ..math_signals.defaults.base_structures import Spectrogram
from ..math_signals.math_signal import Spectrum
from ..math_signals.math_sweep import Sweep
from .named_signal import NamedSignal, NamedSpectrum


InName = Union[HeaderBase, str, Callable[[], str]]


class NamedSweep(NamedSignal):
    def __init__(
        self,
        time: Any,
        amplitude: Any = None,
        name: InName = None,
        category: str = "sweep",
        f_t: Any = None,
        a_t: Any = None,
        aprior_signal: Any = None,
    ) -> None:

        self.header: HeaderSweep = HeaderSweep(name, category)

        self._f_t = (
            super()._convert_input(f_t, self.header) if f_t is not None else None
        )
        self._a_t = (
            super()._convert_input(a_t, self.header) if a_t is not None else None
        )

        self.aprior_signal: Optional[NamedSignal] = (
            aprior_signal if aprior_signal is None else NamedSignal(aprior_signal)
        )

        if isinstance(aprior_signal, Spectrum):
            self.aprior_signal = NamedSignal(
                aprior_signal.get_signal(), name=self.header
            )
        elif isinstance(aprior_signal, NamedSpectrum):
            self.aprior_signal = aprior_signal.get_signal()
        elif isinstance(aprior_signal, NamedRelation):
            self.aprior_signal = NamedSignal(aprior_signal, name=aprior_signal.header)
        elif aprior_signal is not None:
            self.aprior_signal = NamedSignal(aprior_signal, name=self.header)
        else:
            self.aprior_signal = None

        r_f_t = None if self._f_t is None else self._f_t.relation
        r_a_t = None if self._a_t is None else self._a_t.relation
        r_aprior_signal = (
            None if self.aprior_signal is None else self.aprior_signal.relation
        )

        time, amplitude = NamedConfig.extract_input(time, amplitude)
        self._relation = Sweep(time, amplitude, r_f_t, r_a_t, None)

        self._spectrogram: Optional["NamedSpecrogram"] = None
        self.spectrum: Optional[NamedSpectrum] = None

    @property
    def f_t(self) -> NamedRelation:
        if self._f_t is None:
            header = self.header.get_f_t()
            self._f_t = NamedRelation(self.relation.frequency_time, name=header)
        return self._f_t

    @property
    def a_t(self) -> NamedRelation:
        if self._a_t is None:
            header = self.header.get_a_t()
            self._a_t = NamedRelation(self.relation.amplitude_time, name=header)
        return self._a_t

    @property
    def spectrogram(self) -> "NamedSpecrogram":
        if self._spectrogram is None:
            header = self.header.get_spectrogram()
            self._spectrogram = NamedSpecrogram(self._relation.spectrogram, name=header)
        return self._spectrogram

    def set_f_t(self, name: InName = None, category: str = None) -> None:

        header = self.header.get_f_t(name, category)
        self._f_t = NamedRelation(self.relation.frequency_time, name=header)

    def set_a_t(self, name: InName = None, category: str = None) -> None:
        header = self.header.get_a_t(name, category)
        self._a_t = NamedRelation(self.relation.amplitude_time, name=header)

    def set_spectrogram(self, name: InName = None, category: str = None) -> None:
        header = self.header.get_spectrogram(name, category)
        self._spectrogram = NamedSpecrogram(self.relation.spectrogram, name=header)


class NamedSpecrogram:
    def __init__(
        self, spectrogram: Spectrogram, name: InName = None, category: str = None
    ) -> None:
        self.header = HeaderSpectrogram(name, category)
        self.spectrogram = spectrogram

    @property
    def time(self):
        return self.spectrogram.time

    @property
    def frequency(self):
        return self.spectrogram.frequency

    @property
    def spectrogram_matrix(self):
        return self.spectrogram.spectrogram_matrix

    @property
    def category(self):
        return self.header.category
