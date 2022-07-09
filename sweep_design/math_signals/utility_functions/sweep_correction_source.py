from math import sin
from typing import Callable, Optional, TypeVar

import numpy as np
from loguru import logger

from ..math_relation import Relation
from .emd_analyse import get_IMFs_emd
from .tukey import tukey_a_t

Signal = TypeVar("Signal", bound=Relation)


def soft_clip(
    data: np.ndarray, limits: float, percent=0.85, coef: int = 1
) -> np.ndarray:
    """Custom function for correction."""
    hard_limit = limits
    linear_limit = limits * percent

    def select_choice(data: np.ndarray):

        amplitude = abs(data[0])

        if amplitude <= linear_limit:
            return data[1]

        if amplitude >= hard_limit:
            return ((hard_limit / amplitude) ** coef) * data[1]

        scale = hard_limit - linear_limit
        compression = scale * sin(np.pi / 2 * (amplitude - linear_limit) / scale)

        return (((linear_limit + compression) / amplitude) ** coef) * data[1]

    return np.apply_along_axis(select_choice, 1, data)


def get_correction_for_source(
    signal: Signal,
    reaction_mass: float = 1.0,
    limits: float = None,
    limits_persent=0.85,
    limit_iteration: Optional[int] = 10,
    window_percent=0.01,
    coef_function: Callable[[int], float] = lambda x: x,
) -> Signal:

    """Sweep signal correction for realization on the vibration source.

    Steps of corrections:
    1. Calculate displcament from force.
    2. Using EMD find first IMFs of displacement.
    3. Apply suppression amplitudy after limits.
    4. Apply window at the start to ensure a zero first amplitude.
    5. Return сalculated аorce from displacement

    Parametrs:
    > `signal`: `Relation` - signal to be corrected

    > `reaction_mass`: `float` = 1. - reaction mass of source

    > `limits`: `float` = None - displacement limitation of source

    > `limits_persent`: `float` = 0.85 from 0 to 1, determine the limits =
    `limits*limits_persent` up to which the displacement amplitude will
    not changed, after that, the limit amplitude will be changed using the
    `soft_clip` function.

    > `limit_iteration`: int = 10 - iterate corrections.

    > `window_percent`: float = 0.01 - apply window at the initial displacment
    to ensure a zero first amplitude.

    > `coef_function` - function to suppress.

    Returns:
    > `Relation` of Force.

    """
    displacement = signal.integrate().integrate() / reaction_mass
    imfs = get_IMFs_emd(displacement)

    d_array = np.vstack((imfs[0].y, signal.y[1:-1]))
    d_array = np.transpose(d_array)

    cnt = 0
    while True and limits is not None:
        cnt += 1

        logger.info("Iteration of correction: {}", cnt)

        result = soft_clip(d_array, limits, limits_persent, coef_function(cnt))

        force = type(signal)(signal.x[: result.size], result)

        new_displacement = force.integrate().integrate() / reaction_mass

        imfs = get_IMFs_emd(new_displacement)

        new_displacement = imfs[0]

        if np.all(np.abs(new_displacement.y) < limits):
            break

        if limit_iteration is not None and cnt + 1 > limit_iteration:
            break

        d_array = np.vstack((new_displacement.y, force.y[1:-1]))
        d_array = np.transpose(d_array)

    new_displacement = new_displacement.shift(new_displacement.dx * cnt)

    time = new_displacement.x
    window = Relation(time, tukey_a_t(time, time[-1] * window_percent, "left"))

    return (new_displacement * window).diff().diff() * reaction_mass
