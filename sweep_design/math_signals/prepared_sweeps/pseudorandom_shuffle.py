import math
import random

import numpy as np

from ..math_sweep import Sweep
from ..math_uncalcsweep import UncalculatedSweep
from ..utility_functions.tukey import tukey_a_t


class SegmentSmallerDtError(Exception):
    pass


def get_shuffle(
    time: np.ndarray,
    f_start=1.0,
    f_end=101.0,
    length_time_segments=0.5,
    round_number_freqency: int = None,
    time_end=10.0,
    t_tapper=1.0,
) -> Sweep:

    """Create shuffle sweep signal.

    t_tapper in seconds is used to apply tukey function at the end of dwell sweep signal.
    """

    dt = time[1] - time[0]
    time_end = time[-1]

    if dt >= length_time_segments:
        raise SegmentSmallerDtError(
            f"Length of shuffle time segment \
            (length_time_segments - {length_time_segments}) should be grate \
             then sample rate (dt - {dt})"
        )

    n_segments = math.ceil(time_end / length_time_segments)

    if not round_number_freqency:
        f_segment = np.linspace(f_start, f_end, n_segments + 1)
    else:
        f_segment = np.round(
            np.linspace(f_start, f_end, n_segments + 1), round_number_freqency
        )

    random.shuffle(f_segment)

    x = np.linspace(0.0, length_time_segments, math.ceil(length_time_segments / dt) + 1)
    my_cos = np.cos(x * np.pi / length_time_segments - np.pi) / 2 + 1 / 2
    f_t = []
    for f1, f2 in zip(f_segment[:-1], f_segment[1:]):
        f_t.extend((my_cos * (f2 - f1) + f1)[1:])
    f_t = np.array(f_t)

    t_correct = time
    f_t_correct = f_t[:-2]
    a_t = tukey_a_t(t_correct, t_tapper)

    unsw = UncalculatedSweep(t_correct, f_t_correct, a_t)

    return unsw()
