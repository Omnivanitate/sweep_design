from typing import Any, Tuple

import numpy as np
from ...math_signals.defaults.base_structures import BadInputError, RelationProtocol


class ConverError(Exception):
    pass


x = np.ndarray
y = np.ndarray


def extract_input(x: Any, y: Any) -> Tuple[x, y]:
    """Simple data extraction from parameters."""
    if y is None:
        if isinstance(
            x,
            (
                tuple,
                list,
            ),
        ):
            out_x, out_y = np.array(x[0]), np.array(x[1])
        elif isinstance(x, dict):
            data = list(x.values())
            out_x, out_y = np.array(data[0]), np.array(data[1])
        elif isinstance(x, RelationProtocol):
            out_x, out_y = x.get_data()
        else:
            raise ConverError(f"Unable convert data: x - {x} and y - {y}")

    elif isinstance(y, np.ndarray) and isinstance(x, np.ndarray):
        out_x, out_y = x, y
    else:
        out_x, out_y = np.array(x), np.array(y)

    if out_x.size != out_y.size:
        raise BadInputError(
            f"Lengths of array x and array y is not eqaul.\n"
            f"Size of x is {out_x.size}. Size of y is {out_y.size}."
        )
    return out_x, out_y
