import numpy as np
from typing import Any, Callable, Protocol, Sized, Tuple, TypeVar, Union, Type


Num = Union[float, int, complex]
R = TypeVar("R", bound="HeaderRelation")
R2 = TypeVar("R2", bound="HeaderRelation")
SP = TypeVar("SP", bound="HeaderSpectrum")
S = TypeVar("S", bound="HeaderSignal")
SPRN = Union["HeaderSpectrum", "HeaderRelation", Num]
SSPR = Union["HeaderSpectrum", "HeaderSignal", "HeaderRelation"]
SSPRN = Union["HeaderSpectrum", "HeaderSignal", "HeaderRelation", Num]


class HeaderRelation(Protocol):
    @property
    def name(self) -> Callable[[], str]:
        ...

    @property
    def category(self) -> str:
        ...

    def __str__(self) -> str:
        ...

    def select_data(self: R, x_start: Num = None, x_end: Num = None, **kwargs) -> R:
        ...

    def exp(self: R, **kwargs) -> R:
        ...

    def diff(self: R, **kwargs) -> R:
        ...

    def integrate(self: R, **kwargs) -> R:
        ...

    def interpolate_extrapolate(self: R, new_x: np.ndarray, **kwargs) -> R:
        ...

    def shift(self: R, x_shift: Num = 0, **kwargs) -> R:
        ...

    def __add__(self: R, other: Union["HeaderRelation", Num], **kwargs) -> R:
        ...

    def __radd__(self: R, other: Union["HeaderRelation", Num], **kwargs) -> R:
        ...

    def __sub__(self: R, other: Union["HeaderRelation", Num], **kwargs) -> R:
        ...

    def __rsub__(self: R, other: Union["HeaderRelation", Num], **kwargs) -> R:
        ...

    def __mul__(self: R, other: Union["HeaderRelation", Num], **kwargs) -> R:
        ...

    def __rmul__(self: R, other: Union["HeaderRelation", Num], **kwargs) -> R:
        ...

    def __truediv__(self: R, other: Union["HeaderRelation", Num], **kwargs) -> R:
        ...

    def __rtruediv__(self: R, other: Union["HeaderRelation", Num], **kwargs) -> R:
        ...

    def __pow__(self: R, other: Union["HeaderRelation", Num], **kwargs) -> R:
        ...

    def __rpow__(self: R, other: Union["HeaderRelation", Num], **kwargs) -> R:
        ...

    def __iadd__(self: R, other: Union["HeaderRelation", Num], **kwargs) -> R:
        ...

    def __isub__(self: R, other: Union["HeaderRelation", Num], **kwargs) -> R:
        ...

    def __imul__(self: R, other: Union["HeaderRelation", Num], **kwargs) -> R:
        ...

    def __idiv__(self: R, other: Union["HeaderRelation", Num], **kwargs) -> R:
        ...

    def __ipow__(self: R, other: Union["HeaderRelation", Num], **kwargs) -> R:
        ...

    @staticmethod
    def equalize(r1: R, r2: R2) -> Tuple[R, R2]:
        ...

    @classmethod
    def correlate(
        cls: Type[R], r1: "HeaderRelation", r2: "HeaderRelation", **kwargs
    ) -> R:
        ...

    @classmethod
    def convolve(
        cls: Type[R], r1: "HeaderRelation", r2: "HeaderRelation", **kwargs
    ) -> R:
        ...


class HeaderSpectrum(HeaderRelation, Protocol):

    spectrum: Any

    def get_signal(self, recalculate=False, start_time: float = None) -> "HeaderSignal":
        ...

    def get_amp_spectrum(self: R, **kwargs) -> "HeaderRelation":
        ...

    def get_phase_spectrum(self: R, **kwargs) -> "HeaderRelation":
        ...

    def get_reverse_filter(
        self: SP,
        percent: Union[float, int] = 5.0,
        subtrack_phase=True,
        f_start: float = None,
        f_end: float = None,
        **kwargs
    ) -> SP:
        ...

    def add_phase(self: SP, other: SSPR, **kwargs) -> SP:
        ...

    def sub_phase(self: SP, other: SSPR, **kwargs) -> SP:
        ...

    @classmethod
    def get_spectrum_from_amp_phase(
        cls: Type[SP], s1: HeaderRelation, s2: HeaderRelation, **kwargs
    ) -> SP:
        ...

    @classmethod
    def convolve(cls: Type[SP], r1: SSPR, r2: SSPR, **kwargs) -> SP:
        ...

    @classmethod
    def correlate(cls: Type[SP], r1: SSPR, r2: SSPR, **kwargs) -> SP:
        ...

    def __add__(self: SP, a: SSPRN, **kwargs) -> SP:
        ...

    def __sub__(self: SP, a: SSPRN, **kwargs) -> SP:
        ...

    def __mul__(self: SP, a: SSPRN, **kwargs) -> SP:
        ...

    def __truediv__(self: SP, a: SSPRN, **kwargs) -> SP:
        ...

    def __pow__(self: SP, a: SSPRN, **kwargs) -> SP:
        ...


class HeaderSignal(HeaderRelation, Protocol):
    def get_spectrum(self, recalculate=False, is_start_zero=False) -> "HeaderSpectrum":
        ...

    def get_reverse_signal(
        self: S,
        percent: Union[float, int] = 5.0,
        subtrack_phase: bool = True,
        f_start: float = None,
        f_end: float = None,
        **kwargs
    ) -> S:
        ...

    def add_phase(self: S, other: SSPR, **kwargs) -> S:
        ...

    def sub_phase(self: S, other: SSPR, **kwargs) -> S:
        ...

    @classmethod
    def convolve(cls: Type[S], r1: SSPR, r2: SSPR, **kwargs) -> S:
        ...

    @classmethod
    def correlate(cls: Type[S], r1: SSPR, r2: SSPR, **kwargs) -> S:
        ...

    def __add__(self: S, a: SSPRN, **kwargs) -> S:
        ...

    def __sub__(self: S, a: SSPRN, **kwargs) -> S:
        ...

    def __mul__(self: S, a: SSPRN, **kwargs) -> S:
        ...

    def __truediv__(self: S, a: SSPRN, **kwargs) -> S:
        ...

    def __pow__(self: S, a: SSPRN, **kwargs) -> S:
        ...


class HeaderSpectrogram(Protocol):
    t: np.ndarray
    f: np.ndarray
    S: np.ndarray


class HeaderSweep(HeaderSignal, Protocol):
    f_t: HeaderRelation
    a_t: HeaderRelation
    spectrogram: HeaderSpectrogram
    aprior_signal: HeaderSignal
