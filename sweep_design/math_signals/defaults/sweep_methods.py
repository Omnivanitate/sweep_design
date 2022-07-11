from typing import Any, Callable, Optional, Tuple, Union

import numpy as np
from scipy import integrate  # type: ignore
from scipy.signal import hilbert, spectrogram  # type: ignore

from ...config.config import Config
from ..defaults.base_structures import BadInputError, RelationProtocol
from ..math_relation import Relation
from ..math_signal import Signal, Spectrum

InterpolateTime = Callable[[np.ndarray], np.ndarray]
CallFtatMethod = Callable[[Spectrum], Tuple[np.ndarray, np.ndarray, np.ndarray]]
Ftat = Union[np.ndarray, Callable[[np.ndarray], np.ndarray]]
Ftatr = Union[Relation, Ftat]

frequency = np.ndarray
time = np.ndarray
spectrogram_ = np.ndarray
envelope = np.ndarray

theta = np.ndarray


def simple_freq2time(spectrum: "Spectrum") -> Tuple[time, frequency, envelope]:
    """The simple method to extract frequency modulation from a prior spectrum.

    Properties:
    > spectrum: Spectrum

    Returns:
    > Tuple [
    >> time: np.ndarray,
    >> frequency: np.ndarray,
    >> amplitude_modulation: np.ndarray
    >]

    The amplitude modulation is constant.
    """
    amplitude_spectrum = spectrum.get_amp_spectrum()
    frequency, amplitude = amplitude_spectrum.get_data()
    n_spec = amplitude**2
    time = np.append(
        [0.0], ((n_spec[1:] + n_spec[:-1]) / (frequency[1:] - frequency[:-1])).cumsum()
    )
    coef = amplitude_spectrum.get_norm()
    amplitude_modulation = coef * np.ones(len(time))
    return time, frequency, amplitude_modulation


def pre_interpolate_time(
    x: Union[RelationProtocol, np.ndarray], y: np.ndarray = None
) -> InterpolateTime:
    """Thr interpolation of frequency and amplitude modulation functions.

    The method returns the interpolation function for frequency modulation
    and amplitude envelope. Since the sampling step is not the same,
    it is required to bring the desired sweep signal to the time axis.
    """
    if isinstance(x, Relation):
        x, y = x.get_data()

    def interpolate_time(time):
        nT = x * (time[-1] / x[-1])
        y2 = Config.interpolate_extrapolate_method(nT, y)
        return y2(time)

    return interpolate_time


# conversion adaptive sweep spectra FROM Ampl(freq) TO Freq(time)


def convert_freq2time(
    spectrum: "Spectrum", convert_method: CallFtatMethod
) -> Tuple[InterpolateTime, InterpolateTime]:
    """The method consists in obtaining the functions of frequency and amplitude modulation."""
    nT, f, a_t = convert_method(spectrum)
    return pre_interpolate_time(nT, f), pre_interpolate_time(nT, a_t)


def get_info_from_aprior_data(
    t: Any, aprior_data: Any, f_a_t_method: CallFtatMethod
) -> Tuple[InterpolateTime, InterpolateTime, "Signal"]:
    """Get the frequency and amplitude modulation function from a prior data."""
    if isinstance(t, Spectrum):
        aprior_signal = t.get_signal()
        aprior_spectrum = t
    elif isinstance(t, Relation):
        aprior_signal = Signal(t)
        aprior_spectrum = aprior_signal.get_spectrum()
    elif isinstance(aprior_data, Spectrum):
        aprior_signal = aprior_data.get_signal()
        aprior_spectrum = aprior_data
    elif isinstance(aprior_data, Signal):
        aprior_signal = aprior_data
        aprior_spectrum = aprior_data.get_spectrum()
    elif isinstance(aprior_data, Relation):
        aprior_spectrum = Spectrum(aprior_data)
        aprior_signal = aprior_spectrum.get_signal()
    else:
        aprior_signal = Signal(t, aprior_data)
        aprior_spectrum = aprior_signal.get_spectrum()

    f_t, a_t = convert_freq2time(aprior_spectrum, f_a_t_method)

    return f_t, a_t, aprior_signal


def _extract_x_t(
    t: Optional[np.ndarray], x_t: Ftatr
) -> Tuple[Optional[np.ndarray], InterpolateTime]:

    if not callable(x_t):
        if isinstance(x_t, Relation):
            t, _ = x_t.get_data()
            b_x_t = pre_interpolate_time(x_t)
        else:
            if isinstance(t, np.ndarray) and isinstance(x_t, np.ndarray):
                if t.size != x_t.size:
                    calc_t = np.linspace(t[0], t[-1], x_t.size)
                    x_t = Config.interpolate_extrapolate_method(calc_t, x_t)
                    x_t = x_t(t)
                b_x_t = pre_interpolate_time(t, x_t)
            else:
                raise BadInputError("Not enough data: t or x_t")
    else:
        b_x_t = x_t
    return t, b_x_t


def get_info_from_ftat(
    t: Optional[np.ndarray], f_t: Optional[Ftatr], a_t: Optional[Ftatr]
) -> Tuple[Optional[np.ndarray], InterpolateTime, InterpolateTime]:
    """ """
    if f_t is None:

        def linear_time(time: np.ndarray) -> np.ndarray:
            return time

        f_t = linear_time

    t1, f_t = _extract_x_t(t, f_t)

    if a_t is None:

        def const_one(time: np.ndarray) -> np.ndarray:
            return np.ones(len(time))

        a_t = const_one

    t2, a_t = _extract_x_t(t, a_t)

    if t is None:
        if t1 is None and t2 is not None:
            t = t2
        elif t2 is None and t1 is not None:
            t = t1
        elif t2 is not None and t1 is not None:
            t = Config.get_common_x(t1, t2)

    return t, f_t, a_t


# ==============================================================================


def get_spectrogram(
    time: np.ndarray, amplitude: np.ndarray, dt: float = None
) -> Tuple[time, frequency, spectrogram_]:
    """Function to get spectrogram of the sweep signal.

    Using the scipy.signal.spectrogram function.
    """
    if dt is None:
        dt = time[1] - time[0]

    frequency, spectrogram_time, spectrogram_ = spectrogram(amplitude, 1 / (dt))

    return spectrogram_time, frequency, spectrogram_


def get_f_t(time: np.ndarray, amplitude: np.ndarray) -> Relation:
    """Get time-frequency function from sweep signal using the Hilbert transformation.

    Using the scipy.signal.hilbert function.
    """
    analytical_signal = hilbert(amplitude)
    result = np.append(
        [0.0],
        np.diff(np.unwrap(np.angle(analytical_signal)))
        / (2.0 * np.pi)
        / (time[1] - time[0]),
    )
    return Relation(time, result)


def get_a_t(time: np.ndarray, amplitude: np.ndarray) -> Relation:
    """Get envelop from sweep signal using the Hilbert transformation.

    Using the scipy.signal.hilbert function.
    """
    analytical_signal = hilbert(amplitude)
    return Relation(time, np.abs(analytical_signal))


def integrate_quad(
    f_t_function: Callable[[time], frequency], time: np.ndarray
) -> theta:
    """Integration.

    Integration of time-frequency function, using scipy.integrate.quad function.
    """
    return np.append(
        [0.0],
        np.array(
            [2 * np.pi * integrate.quad(f_t_function, time[0], t)[0] for t in time[1:]]
        ),
    )
