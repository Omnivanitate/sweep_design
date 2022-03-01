from typing import Any, Callable, Union, Tuple

import numpy as np

from compose_signals.c_sweep import ComposedSweep
from math_signals.math_uncalcsweep import UncalculatedSweep, ApriorUncalculatedSweep
from header_signals.base_header import NamedBase
from header_signals.uncalcsweep_header import NamedUncalcSweep, NamedApriorUcalcSweep
from math_signals.math_signal import Spectrum

InName = Union[NamedBase, str, Callable[[], str]]

CallFtatMethod = Callable[[Spectrum], Tuple[np.ndarray, np.ndarray, np.ndarray]]

class ComposedUncalcSweep:
    
    def __init__(self, t: Any = None, f_t: Any = None, a_t: Any = None, 
        name: InName = None, category: str = None) -> None:

        self.uncalcsweep = UncalculatedSweep(t, f_t, a_t)
        self.header = NamedUncalcSweep(name, category)
          
    def __call__(self, time: Any = None, tht0 = 0., name: InName = None, category: str = None) ->  ComposedSweep:
        sweep = self.uncalcsweep(time, tht0)
        header = self.header(sweep._x, name, category)    
        return ComposedSweep(sweep, name = header)
    
    
class ComposedApriorUncalcSweep(ComposedUncalcSweep):
    
    def __init__(self, t: Any = None, aprior_data: Any = None, 
        ftat_method: CallFtatMethod = None,
        name: InName = None, category: str = None) -> None:
        
        self.uncalcsweep = ApriorUncalculatedSweep(t, aprior_data, ftat_method)
        self.header = NamedApriorUcalcSweep(name, category)
