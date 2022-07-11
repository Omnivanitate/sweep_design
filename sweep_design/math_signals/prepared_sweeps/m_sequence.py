import numpy as np
from scipy.signal import butter, filtfilt, max_len_seq

from ..math_relation import Relation
from ..math_signal import Signal
from ..utility_functions import get_IMFs_ceemdan, tukey_a_t
import math
import random


def filtering(seq: Signal, f: float, type_filter: str):

    b, a = butter(3, f * 2 * seq.dx, type_filter)
    x, y = seq.get_data()
    y2 = filtfilt(b, a, y)
    return Signal(x, y2)


def get_m_sequence(
    len_seq: float,
    dt: float,
    reaction_mass: float = 1,
    displacement_limit: float = 1,
    force_limit: float = 1000,
    t_tapper=1.0,
    f_start=None,
    f_end=None,
    is_full=False,
) -> np.ndarray:

    start_len_seq = math.ceil(math.log((len_seq - 1), 2))
    start_seq = np.array([random.randint(0, 1) for _ in range(start_len_seq)])

    m_seq = max_len_seq(nbits=start_seq.size, state=start_seq)[0]
    t = np.linspace(0, dt * (m_seq.size - 1), m_seq.size)
    signal = 2 * Signal(t, m_seq) - 1

    if f_start is not None:
        signal = filtering(signal, f_start, "highpass")

    if f_end is not None:
        signal = filtering(signal, f_end, "lowpass")

    displacement = signal.integrate().integrate()

    imfs = get_IMFs_ceemdan(displacement)

    result_signal = sum(imfs[:-1])
    y = result_signal.y * tukey_a_t(result_signal.x, t_tapper)
    result_signal = Signal(result_signal.x, y)

    max_displacement: float = np.max(np.abs(result_signal.y))

    result_signal = result_signal / max_displacement * displacement_limit

    result_signal = result_signal.diff().diff() * reaction_mass

    max_force = np.max(np.abs(result_signal.y))

    if max_force > force_limit:
        result_signal = result_signal / max_force * force_limit

    if is_full:
        return result_signal

    return result_signal.select_data(x_end=(len_seq - 1) * dt)


def get_pure_m_sequence(len_seq: float, dt: float) -> Relation:

    len_seq = math.ceil(math.log((len_seq - 1), 2))
    start_seq = np.array([random.randint(0, 1) for _ in range(len_seq)])

    m_seq = max_len_seq(nbits=start_seq.size, state=start_seq)[0]
    t = np.linspace(0, dt * (m_seq.size - 1), m_seq.size)
    return Signal(t, m_seq)
