import logging
from typing import Any, Protocol, Tuple, runtime_checkable


import numpy as np

from math_signals.defaults.base_structures import BadInputError, BaseXY

@runtime_checkable
class GetData(Protocol):

    def get_data(self) -> Tuple[np.ndarray, np.ndarray]: ...


def extract_input(x: Any, y: Any) -> BaseXY:
    
    if y is None:
        if isinstance(x, (tuple, list,)):
            x, y = np.array(x[0]), np.array(x[1])
        elif isinstance(x, dict):
            x = list(x.values())
            x, y = np.array(x[0]), np.array(x[1])
        elif isinstance(x, GetData):
            x, y = x.get_data()   
    
    # dt = x[1]-x[0]
    # for x1, x2 in zip(x[:-1], x[1:]):
    #     if x2-x1 != dt:
    #         logging.warning('Sample rate of array x is not equal.')

    if x.size != y.size:
        raise BadInputError(f'Lengths of array x and array y is not eqaul.\n' \
        f'Size of x is {x.size}. Size of y is {y.size}.')
    return BaseXY(x=np.array(x), y=np.array(y))

