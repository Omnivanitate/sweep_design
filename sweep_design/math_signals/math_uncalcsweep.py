import logging
from math import sqrt
from typing import Any, Callable, Tuple, Union

import numpy as np
from numpy.typing import NDArray

from ..config.sweep_config import SweepConfig

from .defaults import sweep_methods as dfsm
from .defaults.base_structures import BadInputError
from .defaults.sweep_methods import Ftatr
from .math_relation import Relation
from .math_signal import Spectrum
from .math_sweep import Sweep

CallFtatMethod = Callable[[Spectrum], Tuple[np.ndarray, np.ndarray, np.ndarray]]


class UncalculatedSweep:
    """The `UncalculatedSweep` class prepares for the calculation of the signal sweep (`Sweep`).

    The get_info_from_ftat function is used to extract the frequency versus
    `time` and amplitude versus time functions from the passed `frequency_time`
    and `amplitude_time` parameters.

    **Properties**:

    > **time**: `Union[RelationProtocol, NDArray]` = `None`
    The Relation class, or a class derived from the Relation class, or
    an array_like object containing numbers(real or complex).

    > **frequency_time**: `Ftatr` = `None`
    This parameter, which describes changes in frequency over time,
    can be either an array_like, or an object from which an instance
    of the `Relation` class will be created, or an instance of the
    `Relation` class, or a callable object that returns a numeric sequence.
    If `None`, then the linear function f = t will be used.

    > **amplitude_time**: `Ftatr` = `None`
    This parameter, which describes changes in amplitude modulation
    over time, can be either an array_like, or an object from which
    an instance of the `Relation` class will be created, or an instance
    of the `Relation` class, or a callable object that
    returns a numeric sequence.
    If `None`, then the function will be assumed to be constant
    and equal to 1.

    """

    def __init__(
        self,
        time: NDArray = None,
        frequency_time: Union[Ftatr, NDArray] = None,
        amplitude_time: Union[Ftatr, NDArray] = None,
    ) -> None:

        self._integrate_function_default = SweepConfig.integrate_function

        time = time if time is None else np.array(time)
        if not (
            isinstance(frequency_time, (np.ndarray, Relation))
            or callable(frequency_time)
            or frequency_time is None
        ):
            frequency_time = np.array(frequency_time)

        if not (
            isinstance(amplitude_time, (np.ndarray, Relation))
            or callable(amplitude_time)
            or amplitude_time is None
        ):
            amplitude_time = np.array(amplitude_time)

        (
            self._time,
            self._frequency_time,
            self._amplitude_time,
        ) = dfsm.get_info_from_ftat(time, frequency_time, amplitude_time)

    def __call__(self, time: NDArray = None, tht0=0.0) -> Sweep:
        """Calling an instance of the class to calculate the sweep signal.

        Properties:

        > **time**: `NDArray` = `None`
        The number sequence determines the time.

        > **tht0**: `float` = 0.
        Zero phase.

        Return
        > `Sweep`
        Returns an instance of the Sweep class - the calculated sweep signal.

        If time is not passed or equals None, then the time sequence created
        when the class instance was initialized will be used.

        """
        logging.info(
            "Calling uncalculated sweep.\n"
            "with params:\nfrequency_time={0}\namplitude_time={1}\ntime={2}"
            "".format(self._frequency_time, self._amplitude_time, time)
        )

        if time is None and self._time is None:
            raise BadInputError("Not enough data: time")

        elif time is None and self._time is not None:
            calc_time = self._time
        elif time is not None:
            calc_time = time

        if self._frequency_time.__name__ == "interpolate_time":
            tht = self._array_tht(self._frequency_time(calc_time))
        else:
            tht = self._func_tht(self._frequency_time)

        sweep = self._amplitude_time(calc_time) * np.sin(tht(calc_time) + tht0)

        amplitude_time = Relation(calc_time, self._amplitude_time(calc_time))
        frequency_time = Relation(calc_time, self._frequency_time(calc_time))

        return Sweep(
            time=calc_time,
            amplitude=sweep,
            frequency_time=frequency_time,
            amplitude_time=amplitude_time,
        )

    def _func_tht(
        self, frequency_time: Callable[[np.ndarray], np.ndarray]
    ) -> Callable[[np.ndarray], np.ndarray]:
        """Functional representation of angular sweep."""

        def result(time: np.ndarray) -> np.ndarray:
            return self._integrate_function_default(frequency_time, time)

        return result

    def _array_tht(
        self, frequency_time: np.ndarray
    ) -> Callable[[np.ndarray], np.ndarray]:
        """Angular sweep represented by a numerical sequence."""

        def result(time: np.ndarray) -> np.ndarray:
            frequency_time_relation = Relation(time, frequency_time)
            return np.append([0.0], 2 * np.pi * frequency_time_relation.integrate().y)

        return result


class ApriorUncalculatedSweep(UncalculatedSweep):
    """`ApriorUncalculatedSweep`

    Class for constructing a sweep signal from a priori data (from another
    signal or spectrum).

    The calculation of the change in frequency with time (`frequency_time`)
    and the amplitude envelope with time (`amplitude_time`) will depend on
    the a priori data (`aprior_data`) and on the method (`ftat_method`)
    by which they will be calculated.

    If the conversion method (`ftat_method`) is not defined or `None`,
    then the method is taken from the `SweepConfig` class `freq2time`.
    Method can be overridden if necessary
    (`sweep_design.math_signals.config.SweepConfig.freq2time`).
    The extracted frequency over time (`frequency_time`) and the amplitude
    envelope over time (`amplitude_time`) will be send to the
    `UncalculatedSweep` constructor.
    """

    def __init__(
        self,
        time: Any = None,
        aprior_data: Any = None,
        ftat_method: CallFtatMethod = None,
    ) -> None:

        if not ftat_method:
            ftat_method = SweepConfig.freq2time

        (
            frequency_time,
            amplitude_time,
            self._aprior_signal,
        ) = dfsm.get_info_from_aprior_data(time, aprior_data, ftat_method)
        super().__init__(time, frequency_time, amplitude_time)

    def __call__(self, time: Any = None, tht0=0.0, is_normolize=True) -> Sweep:
        """Calculate the sweep and normolise it."""
        sweep = super().__call__(time=time, tht0=tht0)

        if is_normolize:
            norm_sweep = sweep.get_norm()
            norm_aprior = self._aprior_signal.get_norm()
            norm = sqrt(norm_aprior) / sqrt(norm_sweep)
            sweep.amplitude_time *= norm
            sweep *= norm

        sweep.aprior_signal = self._aprior_signal
        return sweep
