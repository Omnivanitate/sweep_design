from typing import Any, Callable, Tuple, Union

import numpy as np

from ..math_signals.math_signal import Spectrum
from ..math_signals.math_uncalcsweep import ApriorUncalculatedSweep, UncalculatedSweep
from .header_signals.base_header import HeaderBase
from .header_signals.uncalcsweep_header import NamedApriorUcalcSweep, NamedUncalcSweep
from .named_sweep import NamedSweep

InName = Union[HeaderBase, str, Callable[[], str]]

CallFtatMethod = Callable[[Spectrum], Tuple[np.ndarray, np.ndarray, np.ndarray]]


class ComposedUncalcSweep:
    def __init__(
        self,
        t: Any = None,
        f_t: Any = None,
        a_t: Any = None,
        name: InName = None,
        category: str = None,
    ) -> None:

        self.uncalcsweep = UncalculatedSweep(t, f_t, a_t)
        self.header = NamedUncalcSweep(name, category)

    def __call__(
        self, time: Any = None, tht0=0.0, name: InName = None, category: str = None
    ) -> NamedSweep:
        sweep = self.uncalcsweep(time, tht0)
        header = self.header(sweep._x, name, category)
        return NamedSweep(sweep, name=header)


class ComposedApriorUncalcSweep(ComposedUncalcSweep):
    def __init__(
        self,
        t: Any = None,
        aprior_data: Any = None,
        ftat_method: CallFtatMethod = None,
        name: InName = None,
        category: str = None,
    ) -> None:

        self.uncalcsweep = ApriorUncalculatedSweep(t, aprior_data, ftat_method)
        self.header = NamedApriorUcalcSweep(name, category)
