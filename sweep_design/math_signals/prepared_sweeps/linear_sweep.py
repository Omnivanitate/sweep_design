import numpy as np

from ..math_uncalcsweep import UncalculatedSweep
from ..math_sweep import Sweep
from ..utility_functions.tukey import tukey_a_t
from ..utility_functions import f_t_linear_array


def get_linear_sweep(t: np.ndarray, f_start=1.0, f_end=100.0, t_tapper=1.0) -> Sweep:
    """Create linear sweep.

    t_tapper in seconds is used to apply tukey function to a sweep signal.
    """

    f_t = f_t_linear_array(t, f_start, f_end)
    a_t = tukey_a_t(t, t_tapper)

    unsw = UncalculatedSweep(t, f_t, a_t)
    return unsw()
