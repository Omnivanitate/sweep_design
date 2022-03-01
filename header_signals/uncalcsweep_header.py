from typing import Union, Callable, Any

import numpy as np

from header_signals .base_header import NamedBase
from header_signals.sweep_header import NamedSweep
import header_signals.defaults.names as dfn

InName = Union[NamedBase, str, Callable[[], str]]

class NamedUncalcSweep(NamedBase):

    _quantity = 1

    def __init__(self, name: InName = None, category: str = None) -> None:
        
        if name is None:
            name = dfn.default_name_uncalc_sweep(NamedUncalcSweep._quantity)
            NamedUncalcSweep._quantity += 1

        if category is None:
            category = 'c_sweep'

        super().__init__(name, category)
    
    @property
    def category(self) -> str:
        return self._category

    @category.setter
    def category(self, value) -> None:
        self._category = value

    @property
    def name(self) -> Callable[..., str]:
        return self._name

    @name.setter
    def name(self, value: InName) -> None:
        if callable(value) and isinstance(value(), str):
            self._name = value
        elif isinstance(value, NamedBase):
            self._name = value._name
        else:
            str(value)

            def call() -> str:
                return str(value)
            self._name = call

    def __call__(self, time: np.ndarray, name: InName = None, category: str = None) -> NamedSweep:
        
        if name is None:
            dt = time[1]-time[0]
            T = time[-1]-time[0]
            name = dfn.default_name_call_uncalc_sweep(dt, T, self)
        
        if category is None: 
            category = self.category

        return NamedSweep(name = name, category = category)

class NamedApriorUcalcSweep(NamedUncalcSweep):

    _quantity = 1
    
    def __init__(self, name: InName = None, category: str = None) -> None:

        if name is None:
            name = dfn.default_name_aprior_uncalc_sweep(NamedApriorUcalcSweep._quantity)
            NamedApriorUcalcSweep._quantity += 1

        if category is None:
            category = 'c_sweep'

        super().__init__(name, category)
