from typing import Literal
import numpy as np
from scipy.signal.windows import tukey


def tukey_a_t2(time: np.ndarray, t_tapper: float) -> np.ndarray:
    """Tukey function to build the envelop for sweep signal.

    Parametrs:
    > time: np.ndarray - time axis
    > t_tapper: float - shape of tukey window in time.
    Returns:
    > envelope: np.ndarray
    """

    if t_tapper <= time[int(time.size / 2)]:
        tapper = time[time <= t_tapper].size * 2 / time.size
    else:
        tapper = 1.0
    return tukey(time.size, alpha=tapper)


def tukey_a_t(
    time: np.ndarray,
    t_tapper: float,
    location: Literal["left", "right", "both"] = "both",
):

    if t_tapper <= time[int(time.size / 2)]:
        tapper = time[time <= t_tapper].size * 2 / time.size
    else:
        tapper = 1.0

    result = tukey(time.size, alpha=tapper)

    if location == "both":
        return result

    result = np.append(
        result[: int(time.size / 2)], np.ones(time.size - int(time.size / 2))
    )

    if location == "left":
        return result

    if location == "right":
        return np.flip(result)

    return np.ones(time.size)
