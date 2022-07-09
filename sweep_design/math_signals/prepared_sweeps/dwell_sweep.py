import numpy as np

from ..math_relation import Relation
from ..math_sweep import Sweep
from ..math_uncalcsweep import ApriorUncalculatedSweep
from ..utility_functions.ftat_functions import dwell
from ..utility_functions.tukey import tukey_a_t


def get_dwell_sweep(
    t: np.ndarray,
    f_start=1.0,
    f_central=5.0,
    f_end=100.0,
    t_tapper=1.0,
    aprior_data: Relation = None,
) -> Sweep:
    """Create a dwell sweep using an a priori data.

    t_tapper in seconds is used to apply tukey function at the end of dwell sweep signal.
    """
    ftat_method = dwell(f_start, f_end, f_central)
    tukey_coef = np.append(
        np.ones(int(len(t) / 2)), tukey_a_t(t, t_tapper)[int(len(t) / 2) + 1 :]
    )
    uasw = ApriorUncalculatedSweep(t, aprior_data, ftat_method)

    return tukey_coef * uasw()
