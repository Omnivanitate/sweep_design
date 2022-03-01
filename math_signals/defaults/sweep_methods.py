from math import sqrt
from typing import Callable, Optional, Protocol, Union, Tuple, Any, runtime_checkable

import numpy as np
from scipy import integrate # type: ignore 
from scipy.signal import hilbert, spectrogram # type: ignore

from math_signals.defaults.base_structures import BadInputError, Spectrogram, RelationProtocol
from math_signals.math_relation import Relation
from math_signals.math_signal import Signal, Spectrum



I = Callable[[np.ndarray], np.ndarray]
CallFtatMethod = Callable[[Spectrum], Tuple[np.ndarray, np.ndarray, np.ndarray]]
Ftat = Union[np.ndarray, Callable[[np.ndarray], np.ndarray]]
Ftatr = Union[Relation, Ftat]


def simple_freq2time(spectrum: 'Spectrum') -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    f, A = spectrum.get_amp_spectrum().get_data()
    n_spec = A ** 2
    nT = np.append([0.], ((n_spec[1:]+n_spec[:-1])/(f[1:]-f[:-1])).cumsum())
    coef = integrate.trapz(n_spec, f)
    a_t = sqrt(coef*2)*np.ones(len(nT))
    return nT, f, a_t


def pre_interpolate_time(x: Union[RelationProtocol, np.ndarray], y: np.ndarray = None) -> I:
    if isinstance(x, Relation):
        x, y = x.get_data()

    def interpolate_time(time):
        nT = x*(time[-1]/x[-1])
        y2 = Relation.interpolate_extrapolate_method_default(nT, y)
        return y2(time)
    return interpolate_time

# conversion adaptive sweep spectra FROM Ampl(freq) TO Freq(time)

def convert_freq2time(spectrum: 'Spectrum', convert_method: CallFtatMethod) -> Tuple[I, I]:
    nT, f, a_t = convert_method(spectrum)
    return pre_interpolate_time(nT, f), pre_interpolate_time(nT, a_t)


def get_info_from_aprior_data(t: Any, aprior_data: Any,
                f_a_t_method: CallFtatMethod) -> Tuple[I, I, 'Signal']:

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
    else:
        aprior_signal = Signal(t, aprior_data)
        aprior_spectrum = aprior_signal.get_spectrum()
    
    f_t, a_t = convert_freq2time(aprior_spectrum, f_a_t_method)

    return f_t, a_t, aprior_signal


def extract_x_t(t: Optional[np.ndarray], x_t: Ftatr) -> Tuple[Optional[np.ndarray], I]:

    if not callable(x_t):
        if isinstance(x_t, RelationProtocol):
            t, _ = x_t.get_data()
            b_x_t = pre_interpolate_time(x_t)
        else:
            if isinstance(t, np.ndarray) and isinstance(x_t, np.ndarray):
                if t.size != x_t.size:
                    calc_t = np.linspace(t[0], t[-1], len(x_t))
                    b_x_t = Relation.interpolate_extrapolate_method_default(
                        calc_t, x_t)(t)
            else:
                raise BadInputError('Not enough data: t or x_t')
    else: 
        b_x_t = x_t    
    return t, b_x_t


def get_info_from_ftat(t: Optional[np.ndarray], f_t: Optional[Ftatr], 
                        a_t: Optional[Ftatr]) -> Tuple[Optional[np.ndarray], I, I]:
    if f_t is None:
        def linear_time(time: np.ndarray) -> np.ndarray:
            return time
        f_t = linear_time

    t1, f_t = extract_x_t(t, f_t)

    if a_t is None:
        def const_one(time: np.ndarray) -> np.ndarray:
            return np.ones(len(time))
        a_t = const_one

    t2, a_t = extract_x_t(t, a_t)

    if t is None:
        if t1 is None and t2 is not None:
            t = t2
        elif t2 is None and t1 is not None:
            t = t1
        elif t2 is not None and t1 is not None:
            t = Relation.get_common_x_default(t1, t2)        

    return t, f_t, a_t

#==============================================================================

def get_spectrogram(nperseg=2048, noverlap=1024, nfft=4096) \
                    -> Callable[[np.ndarray, np.ndarray], Spectrogram]:

    def extract(x: np.ndarray, y: np.ndarray) -> Spectrogram:
        dt = x[1]-x[0]
        f, t, S = spectrogram(y, 1/(dt), nperseg=nperseg,
                              noverlap=noverlap, nfft=nfft)

        return Spectrogram(f=f, t=t, S=S)

    return extract


def get_f_t(t: np.ndarray, A: np.ndarray) -> Relation:
    analit_signal = hilbert(A)
    result = np.append([0.], np.diff(np.unwrap(np.angle(analit_signal)))/(2.0*np.pi)/(t[1]-t[0]))
    return Relation(t, result)


def get_a_t(t: np.ndarray, A: np.ndarray) -> Relation:
    analit_signal = hilbert(A)
    return Relation(t, np.abs(analit_signal))
