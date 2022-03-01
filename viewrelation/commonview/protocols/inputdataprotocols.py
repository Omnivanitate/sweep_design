from typing import Protocol, Tuple, runtime_checkable

import numpy as np

@runtime_checkable
class ViewRelation(Protocol):

    @property
    def category(self) -> str: ...
    
    def get_data(self) -> Tuple[np.ndarray, np.ndarray]: ...  

@runtime_checkable
class ViewSignal(ViewRelation, Protocol):

    def get_spectrum(self) -> 'ViewSpectrum': ...

@runtime_checkable
class ViewSpectrum(ViewRelation, Protocol):

    def get_signal(self) -> ViewSignal: ...
    
    def get_amp_spectrum(self) -> ViewRelation: ...

    def get_phase_spectrum(self) -> ViewRelation: ...

@runtime_checkable
class ViewSpectrogram(Protocol):

    @property
    def t(self) -> np.ndarray: ...

    @property
    def f(self) -> np.ndarray: ...

    @property
    def S(self) -> np.ndarray: ...

    @property
    def category(self) -> str: ...

@runtime_checkable
class ViewSweep(ViewSignal, Protocol):

    @property
    def f_t(self) -> ViewRelation: ...

    @property
    def a_t(self) -> ViewRelation: ...

    @property
    def spectrogram(self) -> ViewSpectrogram: ... 

class BaseView(Protocol):

    @property
    def default_entity_property(self) -> dict: ...
    
    def add_line(self) -> None: ...

    def add_image(self) -> None: ...

    def get_next_color(self) -> str: ...
    
    def show(self) -> None: ...