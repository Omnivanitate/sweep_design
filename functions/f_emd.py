from PyEMD import CEEMDAN
from math_signals.math_signal import Signal


def calc_ceemdan(data: Signal):
    x, y = data.get_data()
    emd = CEEMDAN(30)
    IMFs = emd(y)
    result = [Signal(x, k) for k in IMFs]
    return result
