from typing import Any, Union, Callable, Optional

from compose_signals.c_relation import ComposedRelation

from header_signals.base_header import NamedBase
from header_signals.sweep_header import NamedSpectrogram, NamedSweep
from math_signals.defaults.base_structures import Spectrogram
from math_signals.math_signal import Spectrum
from math_signals.math_sweep import Sweep
from compose_signals.c_signal import ComposedSignal, ComposedSpectrum
from compose_signals.c_relation import ComposedRelation

InName = Union[NamedBase, str, Callable[[], str]]


class ComposedSweep(ComposedSignal):
    
    def __init__(self, t: Any, a: Any = None, name: InName = None, 
                    category: str = 'sweep', f_t: Any = None,
                    a_t: Any = None, aprior_signal: Any = None) -> None:

        self.header: NamedSweep = NamedSweep(name, category)

        self._f_t = super()._convert_input(f_t, self.header) if f_t is not None else None
        self._a_t = super()._convert_input(a_t, self.header) if a_t is not None else None

        self.aprior_signal: Optional[ComposedSignal]

        if isinstance(aprior_signal, Spectrum):
            self.aprior_signal = ComposedSignal(aprior_signal.get_signal(), name=self.header)
        elif isinstance(aprior_signal, ComposedSpectrum):
            self.aprior_signal = aprior_signal.get_signal()
        elif isinstance(aprior_signal, ComposedRelation):
            self.aprior_signal = ComposedSignal(aprior_signal, name = aprior_signal.header)
        elif aprior_signal is not None:
            self.aprior_signal = ComposedSignal(aprior_signal, name = self.header)
        else:
            self.aprior_signal = None
    
        r_f_t = None if self._f_t is None else self._f_t.relation
        r_a_t = None if self._a_t is None else self._a_t.relation
        r_aprior_signal = None if self.aprior_signal is None else self.aprior_signal.relation
        
        t, a = self.extract_input_default(t, a)        
        self.relation: Sweep = Sweep(t, a, r_f_t, r_a_t, r_aprior_signal)        
       
        self._spectrogram: Optional['ComposedSpecrogram'] = None
        self.spectrum: Optional[ComposedSpectrum] = None

    @property
    def f_t(self) -> ComposedRelation:
        if self._f_t is None:
            header = self.header.get_f_t()
            self._f_t = ComposedRelation(self.relation.f_t, name=header)
        return self._f_t

    @property
    def a_t(self) -> ComposedRelation:
        if self._a_t is None:
            header = self.header.get_a_t()
            self._a_t = ComposedRelation(self.relation.a_t, name=header)
        return self._a_t
    
    @property
    def spectrogram(self) -> 'ComposedSpecrogram':
        if self._spectrogram is None:
            header = self.header.get_spectrogram()
            self._spectrogram = ComposedSpecrogram(
            self.relation.spectrogram, name=header)
        return self._spectrogram

    def set_f_t(self, name: InName = None, category: str = None) -> None:
        
        header = self.header.get_f_t(name, category)
        self._f_t = ComposedRelation(self.relation.f_t, name=header)
        
    def set_a_t(self, name: InName = None, category: str = None) -> None:
        header = self.header.get_a_t(name, category)
        self._a_t = ComposedRelation(self.relation.a_t, name=header)
        
    def set_spectrogram(self, name: InName=None, 
                                        category: str = None) -> None:
        header = self.header.get_spectrogram(name, category)
        self._spectrogram = ComposedSpecrogram(self.relation.spectrogram, name=header)
    

class ComposedSpecrogram:

    def __init__(self, spectrogram: Spectrogram, name: InName = None, category: str = None) -> None:
        self.header = NamedSpectrogram(name, category)
        self.spectrogram = spectrogram

    @property
    def t(self):
        return self.spectrogram.t

    @property
    def f(self):
        return self.spectrogram.f

    @property
    def S(self):
        return self.spectrogram.S

    @property
    def category(self):
        return self.header.category