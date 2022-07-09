from typing import Optional, TypeVar, Union, Type

import numpy as np
from numpy.typing import NDArray

from ..config import Config
from .math_relation import Relation
from .defaults.base_structures import ConvertingError


Num = Union[float, int, complex]
R = TypeVar("R", bound=Relation)
SP = TypeVar("SP", bound="Spectrum")
S = TypeVar("S", bound="Signal")
SPRN = Union["Spectrum", "Relation", Num]
SSPR = Union["Spectrum", "Signal", "Relation"]
SSPRN = Union["Spectrum", "Signal", "Relation", Num]


def _input2spectrum_operation(inp: SSPRN) -> Union["Relation", "Spectrum", Num]:
    if isinstance(inp, Signal):
        return inp.get_spectrum()
    elif isinstance(inp, (Spectrum, Relation, int, float, complex)):
        return inp
    else:
        raise ConvertingError(type(inp), Spectrum)


def _input2spectrum(inp: SSPR) -> "Spectrum":
    if isinstance(inp, Signal):
        return inp.get_spectrum()

    elif isinstance(inp, Spectrum):
        return inp

    elif isinstance(inp, Relation):
        return Spectrum(inp)
    else:
        raise ConvertingError(type(inp), Spectrum)


class Spectrum(Relation):
    """A class that describes the Fourier spectrum of a signal.

    The `Spectrun` class derived from the `Relation` class.

    **Properties**:

    > **frequency**: `Union[Relation, NDArray]`
    An instance of Relation class or inherited from it, or array_like object
    containing numbers (real or complex).

    > **spectrum_amplitude**: `Oprional[NDArray]`
    None or array_like object containing numbers (real or complex).

    > **df**: `float` = `None`
    Sample rate of frequency-axis

    To convert the spectrum into a signal, the method defined in the Config
    class is used. (Config.spectrum2signal_method). Current method can be
    overridden by own in `Config` class.

    When performing arithmetic operations on instances of the `Signal` class,
    an instance of the `Spectrum` class will be extracted from
    the `Signal` instance, and arithmetic operations will be performed
    on this instance. An instance of `Relation` class will be converted into
    the instance of `Spectrum` class.
    """

    def __init__(
        self,
        frequency: Union[Relation, NDArray],
        spectrum_amplitude: NDArray = None,
        df: float = None,
        **kwargs
    ) -> None:
        super().__init__(frequency, spectrum_amplitude, df)
        self._spectrum2signal_method_default = Config.spectrum2signal_method
        self.signal: Optional[Signal] = None

    @property
    def frequency(self):
        return self.x

    @property
    def spectrum_amplitude(self):
        return self.y

    @property
    def df(self):
        return self.dx

    @df.setter
    def df(self, value: float):
        self.dx = value

    def get_signal(self, recalculate=False, start_time: float = None) -> "Signal":
        """Compute the signal from the spectrum."""

        if self.signal is None or recalculate:
            time, amplitude = self._spectrum2signal_method_default(
                self._x, self._y, start_time
            )
            self.signal = Signal(time, amplitude)
        return self.signal

    def get_amp_spectrum(self: R, **kwargs) -> "Relation":
        """Amplitude spectrum.

        Calculate the relationship between the frequency and the absolute
        value of the spectrum amplitude."""

        x, y = self.get_data()
        return Relation(x, np.abs(y))

    def get_phase_spectrum(self: R, **kwargs) -> "Relation":
        """Calculate the relationship between frequency and phase of the spectrum."""
        x, y = self.get_data()
        return Relation(x, np.unwrap(np.angle(y)))

    def get_reverse_filter(
        self: SP,
        percent: Union[float, int] = 5.0,
        subtrack_phase=True,
        frequency_start: float = None,
        frequency_end: float = None,
        **kwargs
    ) -> SP:
        """Calculate filter of reversed signal.

        **Properties**:
        > **percent**: `Union[float, int]`
        level of added white noise in percent

        **subtrack_phase**: True
        If True performs phase subtraction,
        If False succeeds, add the phase.

        **frequency_start**: `float`**
        Start frequency.

        **frequency_end**: `float`
        End frequency.

        """
        spectrum = self.select_data(frequency_start, frequency_end)
        abs_spectrum = spectrum.get_amp_spectrum()
        abs_spectrum = abs_spectrum + abs_spectrum.max() * percent / 100
        reversed_abs_spectrum = 1 / abs_spectrum

        if subtrack_phase:
            phase_spectrum = -1 * spectrum.get_phase_spectrum()
        else:
            phase_spectrum = 1 * spectrum.get_phase_spectrum()

        result_spectrum = type(self).get_spectrum_from_amp_phase(
            reversed_abs_spectrum, phase_spectrum, **kwargs
        )
        return result_spectrum

    def add_phase(self: SP, other: SSPR, **kwargs) -> SP:
        sp_other = _input2spectrum(other)
        return type(self).get_spectrum_from_amp_phase(
            self.get_amp_spectrum(),
            self.get_phase_spectrum() + sp_other.get_phase_spectrum(),
            **kwargs
        )

    def sub_phase(self: SP, other: SSPR, **kwargs) -> SP:
        sp_other = _input2spectrum(other)
        return type(self).get_spectrum_from_amp_phase(
            self.get_amp_spectrum(),
            self.get_phase_spectrum() - sp_other.get_phase_spectrum(),
            **kwargs
        )

    @classmethod
    def get_spectrum_from_amp_phase(
        cls: Type[SP], s1: Relation, s2: Relation, **kwargs
    ) -> SP:
        """Calculate of the spectrum from the amplitude and frequency spectrum.

        The spectrum is calculated through the amplitude and phase spectrum
        using the formula abs*exp(1j*phase)."""

        return cls(s1 * ((1.0j * s2).exp()), **kwargs)

    @classmethod
    def convolve(cls: Type[SP], r1: SSPR, r2: SSPR, **kwargs) -> SP:
        sp_r1 = _input2spectrum(r1)
        sp_r2 = _input2spectrum(r2)
        return super().convolve(sp_r1, sp_r2, **kwargs)

    @classmethod
    def correlate(cls: Type[SP], r1: SSPR, r2: SSPR, **kwargs) -> SP:
        sp_r1 = _input2spectrum(r1)
        sp_r2 = _input2spectrum(r2)
        return super().correlate(sp_r1, sp_r2, **kwargs)

    def __add__(self: SP, a: SSPRN, **kwargs) -> SP:
        r_a = _input2spectrum_operation(a)
        return super().__add__(r_a, **kwargs)

    def __sub__(self: SP, a: SSPRN, **kwargs) -> SP:
        r_a = _input2spectrum_operation(a)
        return super().__sub__(r_a, **kwargs)

    def __mul__(self: SP, a: SSPRN, **kwargs) -> SP:
        r_a = _input2spectrum_operation(a)
        return super().__mul__(r_a, **kwargs)

    def __truediv__(self: SP, a: SSPRN, **kwargs) -> SP:
        r_a = _input2spectrum_operation(a)
        return super().__truediv__(r_a, **kwargs)

    def __pow__(self: SP, a: SSPRN, **kwargs) -> SP:
        r_a = _input2spectrum_operation(a)
        return super().__pow__(r_a, **kwargs)


def _inp2signal_operation(inp: SSPRN) -> Union["Relation", "Signal", Num]:
    if isinstance(inp, Spectrum):
        return inp.get_signal()
    elif isinstance(inp, (Signal, Relation, int, complex, float)):
        return inp
    else:
        raise ConvertingError(type(inp), Signal)


def _inp2signal(inp: SSPR) -> "Signal":
    if isinstance(inp, Spectrum):
        return inp.get_signal()

    elif isinstance(inp, Signal):
        return inp

    elif isinstance(inp, Relation):
        return Signal(inp)
    else:
        raise ConvertingError(type(inp), Signal)


class Signal(Relation):
    """Class describing some kind of signal.

    The `Signal` class inherits the `Relation` class.

    **Properties**:
    > **time**: `Union[Relation, NDArray]`
    An instance of Relation class or inherited from it, or array_like object
    containing numbers (real or complex).

    > **amplitude**: `NDArray`
    None or array_like object containing numbers (real or complex).

    > **dt**: `float` = `None`
    Sample rate of time-axis

    To convert the signal into a spectrum, the method defined in the `Config`
    class is used. (Config.signal2spectrum_method). Current method can be
    overridden by own in Config class.

    When performing arithmetic operations on instances of the Spectrum class,
    an instance of the `Singal` class will be extracted from
    the `Spectrum` instance, and arithmetic operations will be performed
    on this instance. An instance of `Relation` class will be converted into
    the instance of `Signal` class.

    """

    def __init__(
        self,
        time: Union[Relation, np.ndarray],
        amplitude: np.ndarray = None,
        dt: float = None,
    ) -> None:

        self._signal2spectrum_method_default = Config.signal2spectrum_method
        super().__init__(time, amplitude, dt)
        self._spectrum: Optional[Spectrum] = None

    def get_spectrum(self, recalculate=False, is_start_zero=False) -> "Spectrum":

        if self._spectrum is None or recalculate:
            f, a = self._signal2spectrum_method_default(*self.get_data(), is_start_zero)
            self._spectrum = Spectrum(f, a)

        return self._spectrum

    def get_amplitude_spectrum(
        self, recalculate=False, is_start_zero=False
    ) -> Relation:
        return self.get_spectrum(recalculate, is_start_zero).get_amp_spectrum()

    def get_phase_spectrum(self, recalculate=False, is_start_zero=False) -> Relation:
        return self.get_spectrum(recalculate, is_start_zero).get_phase_spectrum()

    def get_reverse_signal(
        self: S,
        percent: Union[float, int] = 5.0,
        subtrack_phase: bool = True,
        frequency_start: float = None,
        frequency_end: float = None,
        **kwargs
    ) -> S:
        """Calculate reversed signal.

        **Properties**:

        > **percent**: `Union[float, int]`
        level of added white noise in percent

        > **subtrack_phase**: True
        If True performs phase subtraction,
        If False succeeds, add the phase.

        > **frequency_start**: float.
        Start frequency.

        > **frequency_end**: float
        End frequency.

        """
        signal = (
            self.get_spectrum()
            .get_reverse_filter(percent, subtrack_phase, frequency_start, frequency_end)
            .get_signal()
        )

        return type(self)(signal, **kwargs)

    def add_phase(self: S, other: SSPR, **kwargs) -> S:
        sp_other = _input2spectrum(other)
        self_spectrum = self.get_spectrum()
        new_spectrum = Spectrum.get_spectrum_from_amp_phase(
            self_spectrum.get_amp_spectrum(),
            self_spectrum.get_phase_spectrum() + sp_other.get_phase_spectrum(),
        )
        return type(self)(new_spectrum.get_signal(), **kwargs)

    def sub_phase(self: S, other: SSPR, **kwargs) -> S:
        sp_other = _input2spectrum(other)
        self_spectrum = self.get_spectrum()
        new_spectrum = Spectrum.get_spectrum_from_amp_phase(
            self_spectrum.get_amp_spectrum(),
            self_spectrum.get_phase_spectrum() - sp_other.get_phase_spectrum(),
        )
        return type(self)(new_spectrum.get_signal(), **kwargs)

    @classmethod
    def convolve(cls: Type[S], r1: SSPR, r2: SSPR, **kwargs) -> S:
        s_r1 = _inp2signal(r1)
        s_r2 = _inp2signal(r2)
        return cls(super().convolve(s_r1, s_r2), **kwargs)

    @classmethod
    def correlate(cls: Type[S], r1: SSPR, r2: SSPR, **kwargs) -> S:
        s_r1 = _inp2signal(r1)
        s_r2 = _inp2signal(r2)
        return cls(super().correlate(s_r1, s_r2), **kwargs)

    def __add__(self: S, a: SSPRN, **kwargs) -> S:
        s_a = _inp2signal_operation(a)
        return super().__add__(s_a, **kwargs)

    def __sub__(self: S, a: SSPRN, **kwargs) -> S:
        s_a = _inp2signal_operation(a)
        return super().__sub__(s_a, **kwargs)

    def __mul__(self: S, a: SSPRN, **kwargs) -> S:
        s_a = _inp2signal_operation(a)
        return super().__mul__(s_a, **kwargs)

    def __truediv__(self: S, a: SSPRN, **kwargs) -> S:
        s_a = _inp2signal_operation(a)
        return super().__truediv__(s_a, **kwargs)

    def __pow__(self: S, a: SSPRN, **kwargs) -> S:
        s_a = _inp2signal_operation(a)
        return super().__pow__(s_a, **kwargs)
