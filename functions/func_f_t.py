from functools import wraps
from typing import Tuple
from math import sqrt

import numpy as np
from scipy import integrate
from scipy.interpolate import interp1d
from math_signals.math_signal import Spectrum


def simple_freq2time(spectrum: 'Spectrum') -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    f, a_f = spectrum.get_amp_spectrum().get_data()
    n_spec = a_f ** 2
    n_t = np.append([0.], ((n_spec[1:]+n_spec[:-1])/(f[1:]-f[:-1])).cumsum())
    coef = integrate.trapz(n_spec, f)
    a_t = sqrt(coef*2)*np.ones(len(n_t))
    return n_t, f, a_t

def dwell(f_start: float = None, f_end: float = None, fc: float = None):

    def freq2time(spectrum: 'Spectrum') -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        
        f, a_f = spectrum.select_data(f_start, f_end).get_amp_spectrum().get_data()

        f_c = fc if fc else f[0] 

        freq = f[f <= f_c]

        freq_ratio = np.divide(
            freq[1:], freq[:-1], out=np.ones_like(freq[1:]), where=freq[:-1] != 0)
        dur = np.cumprod(1/(freq_ratio**4))
        energy = a_f[f <= f_c][:-1]**2
        nT = np.append([0.], dur*energy).cumsum()
        nT2 = np.append(nT[-1], dur[-1]*(a_f[f > f_c]**2)).cumsum()
        nT = np.append(nT, nT2[1:])

        a_t = np.cumprod(np.append([1.], freq_ratio**2))
        a_t = np.append(a_t, [a_t[-1]]
                            * (len(a_f)-len(a_t)))

        return nT, f, a_t

    return freq2time
        

