from typing import TypeVar

import numpy as np

from ..math_relation import Relation
from ..utility_functions.emd_analyse import get_IMFs_emd
from ..utility_functions.tukey import tukey_a_t

Signal = TypeVar("Signal", bound=Relation)


def correct_sweep(signal: Signal, start_window: float = None) -> Signal:
    """Sweep correction.

    Using the EMD to subtract the last IMF from the displacement and apply
    a window in the star so that the displacement starts at zero.
    """

    displacement = signal.integrate().integrate()
    x = displacement.x

    window = tukey_a_t(x, start_window, "left")

    IMFs = get_IMFs_emd(displacement)
    new_displacement = IMFs[0] * Relation(x, window)

    signal = new_displacement.diff().diff()

    return signal


def correct_sweep_without_window(signal: Signal) -> Signal:
    """Using the EMD to subtract the last IMF from the displacement."""
    displacement = signal.integrate().integrate()
    IMFs = get_IMFs_emd(displacement)
    signal = IMFs[0].diff().diff()
    return signal
