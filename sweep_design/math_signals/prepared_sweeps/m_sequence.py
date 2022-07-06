import numpy as np
from scipy.signal import butter, filtfilt, max_len_seq

from ..math_relation import Relation
from ..math_signal import Signal


def get_m_sequence(seq: np.ndarray) -> np.ndarray:
    return max_len_seq(nbits=seq.size, state=seq)[0]

def extend_seq(seq: np.ndarray, points_per_sample: int) -> np.ndarray:
    return np.array([k for k in seq for _ in range(points_per_sample)])

def func_m(seq: np.ndarray, func_array: np.ndarray) -> np.ndarray:
    
        return np.array([k*func_array for k in seq]).flatten()
    
def filtering(f_1, f_2):
    b, a = butter(3, [f_1, f_2], 'band')
    def proc(seq: Signal):
        x, y = seq.get_data()
        y2 = filtfilt(b, a, y)
        return y2
        
    return proc
