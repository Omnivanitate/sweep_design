"""This is where defualt methods are defined."""

from typing import Callable, Union, Any, TYPE_CHECKING, Type, Tuple

import numpy as np
from scipy.interpolate import interp1d  # type: ignore
from scipy.integrate import cumulative_trapezoid, trapz  # type: ignore

from .base_structures import NotEqualError, MathOperation

x = np.ndarray
y = np.ndarray
frequency = np.ndarray
spectrum = np.ndarray
time = np.ndarray
amplitude = np.ndarray

if TYPE_CHECKING:
    from math_signals.math_relation import Relation

Number = Union[float, int, complex]


def math_operation(
    x: np.ndarray,
    y1: np.ndarray,
    y2: Union[np.ndarray, Number],
    name_operation: MathOperation,
) -> Tuple[x, y]:
    """Math operations.

    Using numpy math operations.
    """
    if name_operation == MathOperation.POW:
        y = np.abs(y1).__getattribute__(name_operation.value)(y2) * np.sign(y1)
    else:
        y = y1.__getattribute__(name_operation.value)(y2)

    return x, y


def one_integrate(y: np.ndarray, x: np.ndarray = None) -> float:
    """Integration.

    Taking the integral on a segment. Return of the area under the graph.
    """
    return trapz(y, x)


def integrate(x: np.ndarray, y: np.ndarray, dx: float = None) -> Tuple[x, y]:
    """Integration.

    Using the scipy.integrate.cumtrapz function.
    """
    if dx is None:
        dx = x[1] - x[0]
    return x[1:], cumulative_trapezoid(y) * (dx)


def differentiate(x: np.ndarray, y: np.ndarray, dx: float = None) -> Tuple[x, y]:
    """Differentiation.

    Using the numpy.diff function."""
    if dx is None:
        dx = x[1] - x[0]
    return x[:-1] + (dx) / 2, np.diff(y) / (dx)


def interpolate_extrapolate(
    x: np.ndarray, y: np.ndarray, bounds_error=False, fill_value=0.0
) -> Callable[[x], y]:
    """Interpolation.

    Using the scyipy.interpolate.interp1d function.
    Returning function of interpolation.
    """
    return interp1d(x, y, bounds_error=bounds_error, fill_value=fill_value)


def get_common_x(
    x1: np.ndarray, x2: np.ndarray, dx1: float = None, dx2: float = None
) -> x:
    """Specifies the overall x-axis.

    Finds the general sample rate and beginning and end of sequence.
    """
    if dx1 is None:
        dx1 = x1[1] - x1[0]
    if dx2 is None:
        dx2 = x2[1] - x2[0]
    dx = dx1 if dx1 <= dx2 else dx2
    x_start = x1[0] if x1[0] <= x2[0] else x2[0]
    x_end = x1[-1] if x1[-1] >= x2[-1] else x2[-1]
    X = x_end - x_start
    return np.linspace(x_start, (int(X / dx)) * dx, int(X / dx) + 1)


def correlate(cls: Type["Relation"], r1: "Relation", r2: "Relation") -> Tuple[x, y]:
    """Correlation.

    Using the numpy.correlate function.
    """
    r1 = r1.shift(-r1._x[0])
    r2 = r2.shift(-r2._x[0])
    r1, r2 = cls.equalize(r1, r2)
    x, y1 = r1.get_data()
    _, y2 = r2.get_data()
    return np.append(np.sort(-1 * x)[:-1], x), np.correlate(y1, y2, "full")


def convolve(cls: Type["Relation"], r1: "Relation", r2: "Relation") -> Tuple[x, y]:
    """Convolution.

    Using the numpy.convlove function.
    """
    r1 = r1.shift(-r1._x[0])
    r2 = r2.shift(-r2._x[0])
    r1, r2 = cls.equalize(r1, r2)
    x, y1 = r1.get_data()
    _, y2 = r2.get_data()
    return np.append(np.sort(-1 * x)[:-1], x), np.convolve(y1, y2, "full")


# ==============================================================================


def signal2spectrum(
    time: np.ndarray, amplitude: np.ndarray, is_start_zero=False
) -> Tuple[frequency, spectrum]:
    """Forward Fourier Transform.

    Using the numpy.fft.rfft function.
    """
    if not is_start_zero:
        if time[0] > 0.0:
            time = np.linspace(0.0, time[-1], int(time[-1] / (time[1] - time[0])) + 1)
            amplitude = np.append(np.zeros(time.size - amplitude.size), amplitude)
        elif time[-1] < 0.0:
            time = np.linspace(
                time[0], 0.0, int(abs(time[0]) / (time[1] - time[0])) + 1
            )
            amplitude = np.append(amplitude, np.zeros(time.size - amplitude.size))

        amplitude = np.append(amplitude[time >= 0.0], amplitude[time < 0.0])

    spectrum = np.fft.rfft(amplitude)
    frequency = np.fft.rfftfreq(
        amplitude.size, d=(time[-1] - time[0]) / (amplitude.size)
    )
    return frequency, spectrum


def spectrum2sigmal(
    frequency: np.ndarray, spectrum: np.ndarray, time_start: float = None
) -> Tuple[time, amplitude]:
    """Inverse Fourier Transform.

    Using the numpy.fft.irfft function.
    """
    amplitude = np.fft.irfft(spectrum)  # type: np.ndarray
    if time_start is None:
        time = np.linspace(
            0,
            (amplitude.size - 1) / (2 * (frequency[-1] - frequency[0])),
            amplitude.size,
        )
    else:
        time = np.linspace(
            time_start,
            time_start + (amplitude.size - 1) / (2 * (frequency[-1] - frequency[0])),
            amplitude.size,
        )
        amplitude = np.append(amplitude[time >= 0.0], amplitude[time < 0.0])

    return time, amplitude
