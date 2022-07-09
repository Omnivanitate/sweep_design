from typing import List
from ..math_relation import Relation


def get_code_zinger(
    segment_sweep: Relation, code_zinger: List[int] = [-1, -1, -1, 1], periods=1
):
    """Repeat the transmitted signal according to the Zniger code for n periods (n times)."""

    new_sweep = segment_sweep * code_zinger[0]

    for cnt, v in enumerate(code_zinger[1:], 1):
        new_sweep = new_sweep + v * segment_sweep.shift(
            cnt * segment_sweep.x[-1] + cnt * segment_sweep.dx
        )

    new_sweep_period = new_sweep

    for period in range(periods - 1):
        print(period)
        new_sweep_period += new_sweep.shift(
            (period + 1) * new_sweep_period.x[-1] + (period + 1) * new_sweep_period.dx
        )

    return new_sweep_period
